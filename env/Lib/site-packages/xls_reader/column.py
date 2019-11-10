"""Module with columns and column readers."""
import abc
import configparser
import datetime
import decimal
import enum
import re
import typing

from openpyxl.cell.read_only import ReadOnlyCell

from . import exceptions

__all__ = [
  "ReadOnlyRow",
  "Column",
  "ColumnReader",
  "BaseColumnReader",
  "EnumReader",
  "DatetimeReader",
  "BooleanReader",
  "ColumnDescription",
  "StringReader",
  "DecimalReader",
  "IntegerReader",
]

ReadOnlyRow = typing.Sequence[ReadOnlyCell]
"""
Type that represents a row of read-only cells (used in typing annotations)
"""


InstanceType = typing.Mapping['Column', typing.Any]


_pattern_type = type(re.compile(""))


ColumnDescription = typing.NamedTuple(
  'ColumnDescription',
  (
    ('regex', typing.Union[str, _pattern_type]),
    ('reader', 'ColumnReader')
  )
)


class Column(enum.Enum):
  """
  Abstract base class representing columns in XLS file.
  """

  def __repr__(self):
    return "Column.{}".format(self.name)

  @classmethod
  def get_regex(cls, column: 'Column'):
    """Gets a regex that should match the column"""
    regex = column.value.regex
    if isinstance(regex, str):
      return re.compile(
        r"^\s*" + r"\s*".join(regex.split()) + r"\s*$",
        re.IGNORECASE
      )
    return regex

  @classmethod
  def match_header(cls, column_name: str) -> 'Column':
    """
    Given column header returns column instance. If no such columns exists,
    will raise an exception.
    """
    for column_instance in cls.__members__.values():  # pylint: disable=no-member
      regex = cls.get_regex(column_instance)
      if regex.match(column_name):
        return column_instance
    raise exceptions.UnknownColumnError(column_name)


class ColumnReader(object, metaclass=abc.ABCMeta):
  """Abstract class that reads a column"""

  def __init__(self):
    super().__init__()
    self.required = True

  def read_column(
      self, row: ReadOnlyRow, cell: ReadOnlyCell, instance: InstanceType
  ):
    """
    :param row: full row
    :param cell: Cell from which this Reader should read data
    :param instance: Site instance to modify
    :return:
    """
    raise NotImplementedError

  def pre_checks(self, cell):
    """Does basic checks on cell"""
    pass

  def is_value_empty(self, value) -> bool:
    """Check if value is empty, if True will return None"""
    pass

  def get_value_from_cell(self, cell):
    """Returns and sanitizes value from cell."""
    self.pre_checks(cell)
    if self.is_value_empty(cell.value):
      return None
    return cell.value


class BaseColumnReader(ColumnReader):
  """Base class for column reader"""

  def __init__(
      self,
      *,
      attr_name: str,
      expected_types: typing.Union[None, type, typing.Sequence[type]],
      required: bool = True,
      empty_values: list = None,
      default=None
  ):
    """
    :param attr_name: Value will be set to instance under this attribute
    :param expected_types: List of possible types for cell.value
    :param required: Can cell be empty
    """
    super().__init__()
    if expected_types is None:
      self._expected_types = None
    elif isinstance(expected_types, typing.Sequence):
      self._expected_types = tuple(expected_types)
    else:
      self._expected_types = (expected_types,)
    self.attr_name = attr_name
    self.default = default
    self.required = required

    if empty_values is None:
      empty_values = ["", "??", "n/a", "na", "?"]

    self.empty_values = [x.lower() for x in empty_values]

  @property
  def expected_types(self):
    """
    Return expected types for this column. This should be python types.

    If cell contains different type this will raise an error.
    """
    if self._expected_types is None:
      return None
    if not self.required:
      return self._expected_types + (type(None), )
    return self._expected_types

  def is_value_empty(self, value) -> bool:
    if value is None:
      return True
    if not isinstance(value, str):
      return False
    if value.strip().lower() in self.empty_values:
      return True
    return False

  def pre_checks(self, cell):
    if self.is_value_empty(cell.value):
      if self.required:
        raise exceptions.ColumnReadException("Cell has no value and is required.")
    elif not (self.expected_types is None or isinstance(cell.value, self.expected_types)):
      raise exceptions.ColumnReadException(
        "Cell value is of unexpected type {} (value: {})".format(type(cell.value), cell.value)
      )

  def read_column(self, row: ReadOnlyRow, cell: ReadOnlyCell, instance: dict):
    instance[self.attr_name] = self.get_value_from_cell(cell)


class StringReader(BaseColumnReader):
  """Reader that reads a string."""

  def __init__(self, allow_numbers_as_strings=False, **kwargs):
    kwargs.setdefault("expected_types", (str, ))
    super().__init__(**kwargs)
    self.allow_numbers_as_strings = allow_numbers_as_strings

  @property
  def expected_types(self):
    if self.allow_numbers_as_strings:
      return super().expected_types + (int, float, decimal.Decimal)
    return super().expected_types

  def get_value_from_cell(self, cell):
    if self.is_value_empty(cell.value):
      return None
    return str(super().get_value_from_cell(cell))


class IntegerReader(BaseColumnReader):
  """Reader that reads an integer."""
  def __init__(self, **kwargs):
    kwargs.setdefault("expected_types", (int, float, decimal.Decimal, str))
    super().__init__(**kwargs)

  def get_value_from_cell(self, cell):
    self.pre_checks(cell)
    if self.is_value_empty(cell.value):
      return self.default
    try:
      return int(cell.value)
    except ValueError:
      raise exceptions.ColumnReadException(
        "Can't read cell value as string. Value is: '{}'".format(cell.value)
      )


class DecimalReader(BaseColumnReader):
  """Reader that reads a decimal."""

  def __init__(self, **kwargs):
    kwargs.setdefault("expected_types", (int, float, decimal.Decimal, str))
    super().__init__(**kwargs)

  def get_value_from_cell(self, cell):
    self.pre_checks(cell)
    if self.is_value_empty(cell.value):
      return self.default
    if isinstance(cell.value, decimal.Decimal):
      return cell.value
    if isinstance(cell.value, (float, int, str)):
      try:
        return decimal.Decimal(cell.value)
      except decimal.DecimalException as exception:
        raise exceptions.ColumnReadException(
          "Invalid cell value for decimal cell. Got: {}, type: {}".format(
            cell.value, type(cell.value)
          )
        ) from exception
        # This shouldn't happen as type is verified in pre_checks
    raise exceptions.ColumnReadException(  # pragma: no cover
      "Invalid cell value for decimal cell. Got: {}, type: {}".format(
        cell.value, type(cell.value)
      )
    )


class EnumReader(BaseColumnReader):
  """
  Reads value from spreadsheet and converts it to enum.
  """

  def __init__(
      self,
      attr_name: str,
      enum_type,
      required: bool = True
  ):
    super().__init__(
      attr_name=attr_name,
      required=required,
      expected_types=(str, int, float)
    )
    self.enum_type = enum_type

  def get_from_enum(self, value):
    """Convert cell value to enum."""
    if isinstance(value, str):
      value = value.lower()
    for name, enum_instance in self.enum_type.__members__.items():
      if name.lower() == value:
        return enum_instance
      if enum_instance.value == value:
        return enum_instance
      if isinstance(enum_instance.value, str):
        if enum_instance.value.lower() == value:
          return enum_instance
    raise exceptions.ColumnReadException(
      "Couldn't parse column value '{}', for enum type {}.".format(
        value, self.enum_type
      )
    )

  def get_value_from_cell(self, cell):
    self.pre_checks(cell)
    value = cell.value
    if self.is_value_empty(value):
      return self.default
    if isinstance(value, str):
      value = value.strip()
    return self.get_from_enum(value)


class DatetimeReader(BaseColumnReader):
  """Reads a date/datetime instance."""

  def __init__(self, attr_name: str, required: bool = True):
    super().__init__(
      attr_name=attr_name,
      expected_types=(datetime.date, datetime.datetime),
      required=required
    )

  def pre_checks(self, cell):
    if not self.is_value_empty(cell.value):
      if (self.required and cell.value is None) or not isinstance(cell.value, self.expected_types):
        raise exceptions.ColumnReadException(
          "We have expected date in this cell. Please double-check if Excel didn't format the "
          "column as a string. Cell value: {}".format(cell.value)
        )

    return super().pre_checks(cell)

  @classmethod
  def get_magic_values(cls) -> typing.Mapping[str, datetime.datetime]:
    """
    Sometimes users will insert "magical" values into datetime column,
    like "ready", "done". This allows to map such "magic" strings
    to a corresponding datetime.
    """
    return {}

  def get_value_from_cell(self, cell):
    if isinstance(cell.value, str):
      value = cell.value.lower().strip()
      magic = self.get_magic_values()
      if value in magic:
        return magic[value]
    return super().get_value_from_cell(cell)


class BooleanReader(BaseColumnReader):
  """
  Columns containing a boolean. Will use the same heuristics as ``ConfigParser.getbool``
  """

  def __init__(self, **kwargs):
    kwargs.setdefault('expected_types', (str, bool))
    super().__init__(**kwargs)

  def get_value_from_cell(self, cell):
    if self.is_value_empty(cell.value):
      return self.default
    if isinstance(cell.value, bool):
      return cell.value

    value = str(cell.value).strip().lower()

    if value not in configparser.ConfigParser.BOOLEAN_STATES:
      raise exceptions.ColumnReadException(
        "Invalid value in yes/no column {}".format(value)
      )

    return configparser.ConfigParser.BOOLEAN_STATES[value]

