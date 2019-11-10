"""Data importer."""
import abc
import typing

from openpyxl import load_workbook
from openpyxl.cell.read_only import ReadOnlyCell
from openpyxl.utils import get_column_letter

from .column import (
  Column,
  ColumnReader,
  ReadOnlyRow,
  InstanceType
)

from . exceptions import (
  XLSImportError,
  InvalidHeaderFormat,
  UnknownColumnError,
  InvalidXLSFileException,
  MissingSheetException,
)

__all__ = ['DataImporter']

ColumnMap = typing.Mapping[Column, ColumnReader]


class DataImporter(object):

  """
  Imports an XLS file, we decide what is in given column by reading XLS header,
  which must be first row.
  """

  @classmethod
  @abc.abstractmethod
  def get_column_enum(cls) -> Column:
    """
    Column Enum (contains all possible columns for this XLS file).
    """
    raise NotImplementedError()

  def on_row_read(self, instance: InstanceType):
    """
    Callback that allows customize instance after it was read from the row.
    """
    pass

  @classmethod
  def get_required_columns(cls) -> ColumnMap:
    """
    Returns a dict of columns that are required. Each column is mapped to
    reader that will be used to read this column.
    """
    return {
      column: reader
      for column, reader in cls.get_all_columns().items()
      if reader.required
    }

  @classmethod
  def get_optional_columns(cls) -> ColumnMap:
    """
    Returns a dict of columns that are optional
    """
    return {  # pragma: no cover
      column: reader
      for column, reader in cls.get_all_columns().items()
      if not reader.required
    }

  @classmethod
  def get_all_columns(cls) -> ColumnMap:
    """
    Returns all columns.
    """
    return {
      column: column.value.reader
      for column in cls.get_column_enum().__members__.values()
    }

  def __init__(self, ignore_unknown_columns: bool = False):
    self.column_mappings = None
    """
    A maps a column object to it's index in a XLS file.
    """
    self.column_mappings_reverse = None
    """
    Maps column index in XLS to column type.
    """
    self.ignore_unknown_columns = ignore_unknown_columns

    self.missing_columns = set()
    """
    Set that contains columns that are missing from the XLS.
    """

  def read_file(self, file, sheet: str) -> typing.Iterable[InstanceType]:
    """
    Reads a XLS file.
    """
    workbook = load_workbook(file, read_only=True)

    if sheet not in workbook:
      raise MissingSheetException(
        "No such sheet {}. Available sheets: {}".format(sheet, workbook.get_sheet_names())
      )

    sheet = workbook[sheet]
    yield from self.read_xls(sheet.rows)

  def read_xls(self, rows: typing.Iterable[ReadOnlyRow]):
    """
    Reads a XLS file given an iterable of rows.
    """

    def __is_row_empty(row: ReadOnlyRow):
      for cell in row:
        if isinstance(cell.value, str):
          if cell.value.strip():
            return False
        if cell.value:
          return False
      return True

    row_iterator = enumerate(rows)
    header_idx, header = next(row_iterator)  # pylint: disable=unused-variable
    while __is_row_empty(header):
      header_idx, header = next(row_iterator)  # pylint: disable=unused-variable
    self._make_column_mappings(header)
    for row_idx, row in row_iterator:
      try:
        row = self.parse_row(row)
        if row is not None:
          yield row
      except XLSImportError as exc:
        exc.row = row_idx
        raise exc

  def _make_column_mappings(self, row: ReadOnlyRow):
    """
    Reads a header row and maps column indexes to column instances.
    """
    self.column_mappings = self.map_columns(row)
    self.column_mappings_reverse = {
      v: k for (k, v) in self.column_mappings.items()
    }
    self.missing_columns = set()
    found_columns = self.column_mappings.keys()
    for column, reader in self.get_all_columns().items():
      if column not in found_columns:
        if reader.required:
          raise XLSImportError(
            "Missing required column {}.".format(column)
          )
        else:
          self.missing_columns.add(column)

  def map_columns(
      self,
      headers: typing.Sequence[ReadOnlyCell]
  ) -> typing.Mapping[Column, int]:
    """Given a header row generates mappings Column -> column_index"""
    result = {}
    column_enum = self.get_column_enum()

    def __is_empty(value):
      if value is None:
        return True
      if isinstance(value, str):
        return len(value.strip()) == 0  # pylint: disable=len-as-condition
      return False

    for column_idx, cell in enumerate(headers):
      if __is_empty(cell.value):
        continue

      try:
        column = column_enum.match_header(str(cell.value))
      except UnknownColumnError:
        if not self.ignore_unknown_columns:
          raise
        else:
          continue

      if column in result.keys():
        raise InvalidHeaderFormat("Duplicate column {}".format(column))
      result[column] = column_idx

    return result

  def is_row_empty(self, row: ReadOnlyRow) -> bool:
    """
    Checks if column is empty contains only empty or whitespace rows.
    """
    for index in self.column_mappings.values():
      if index > len(row):
        # End of row
        return True
      value = row[index].value
      if value is None:
        # If column is None we can check other columns
        continue  # pragma: no cover
      if not isinstance(value, str):
        # If column does not contain a string it is not considered empty
        return False
      if value.strip():
        # String is not empty
        return False

    return True

  def is_header_row(self, row: ReadOnlyRow):
    """
    Checks if row is a header row.

    It is used to detect rows that are repetitions of header.
    """
    first_row = min(self.column_mappings.values())
    if not isinstance(row[first_row].value, str):
      return False
    first_column = self.__get_reverse_mappings()[first_row]
    try:
      return self.get_column_enum().match_header(row[first_row].value) == first_column
    except UnknownColumnError:
      return False

  def validate_internal_header(self, row):
    """
    Sometimes there are headers in the middle of the document, we just check
    if they have the same column order as in main XLS. Parsing would be
    a lot more ambiguous if this was not the case.
    """
    for cell in row:
      if not isinstance(cell.value, (str, type(None))):
        raise XLSImportError("All columns should be strings in header rows,")
    internal_header = self.map_columns(row)
    if internal_header != self.__get_column_mappings():
      raise XLSImportError(
        "There was a header in the middle of the document, and it wasn't matching "
        "the main header at the top of the document. Please validate if columns "
        "match in both headers and remove one that is lower in the XLS."
      )

  def get_cell(self, column: Column, row: ReadOnlyRow) -> ReadOnlyCell:
    """
    Returns cell from row using column object.
    """
    if column not in self.column_mappings:
      raise InvalidXLSFileException("Missing column {}".format(column))  # pragma: no cover
    index = self.column_mappings[column]
    return row[index]

  def parse_column(
      self,
      row: ReadOnlyRow,
      column: Column,
      instance: dict,
      required: bool
  ):
    """
    Parses a column and sets read value to an instance.
    """
    if required and column not in self.column_mappings:
      raise InvalidXLSFileException("Missing column {}".format(column))  # pragma: no cover
    if column not in self.column_mappings:
      return
    parser = self.get_all_columns()[column]
    cell = self.get_cell(column, row)
    parser.read_column(row, cell, instance)

  def _parse_row_internal(self, row: ReadOnlyRow):
    """
    Parses whole row and returns parsed instance.
    """
    instance = {}

    required_columns = self.get_required_columns()

    for column in self.get_all_columns():
      try:
        self.parse_column(row, column, instance, column in required_columns)
      except XLSImportError as exc:
        column_id = self.column_mappings.get(column)
        exc.column = get_column_letter(column_id + 1)
        exc.column_enum = column
        raise exc

    for column in self.missing_columns:
      parser = self.get_all_columns()[column]
      mock_cell = ReadOnlyCell(None, None, None, None)
      parser.read_column(row, mock_cell, instance)

    self.on_row_read(instance)

    return instance

  def parse_row(self, row: ReadOnlyRow) -> typing.Optional[dict]:
    """
    Parses a row and saves parsed instance to database.
    """
    if self.is_row_empty(row):
      return None
    if self.is_header_row(row):
      # Sometimes there are copies of header in the XLS, see
      # validate_internal_header for the rest of the explanation.
      self.validate_internal_header(row)
      return None
    return self._parse_row_internal(row)

  def __get_column_mappings(self) -> typing.Mapping[Column, int]:
    return self.column_mappings

  def __get_reverse_mappings(self) -> typing.Mapping[int, Column]:
    return self.column_mappings_reverse
