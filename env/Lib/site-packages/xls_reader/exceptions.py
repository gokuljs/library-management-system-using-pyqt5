"""Exception classes."""

__all__ = [
  "XLSImportError",
  "InvalidHeaderFormat",
  "UnknownColumnError",
  "InvalidXLSFileException",
  "ColumnReadException",

]


class XLSImportError(ValueError):
  """Base class for all XLS import errors"""

  def __init__(
      self,
      message: str,
      row: int = None,
      column: int = None,
      column_enum=None
  ):
    super().__init__()
    self.message = message
    self.row = row
    self.column = column

    self.column_enum = column_enum
    self.args = [self.message]

  def __str__(self, *args, **kwargs):
    self.args = [self.message, self.row, self.column, self.column_enum]
    return super().__str__(*args, **kwargs)


class InvalidHeaderFormat(XLSImportError):
  """Invalid format of header."""


class UnknownColumnError(XLSImportError):
  """Thrown when column header matches no known column"""


class InvalidXLSFileException(XLSImportError):
  """Thrown when XLS has invalid format"""


class ColumnReadException(XLSImportError):
  """Thrown when for any error when reading a column"""
  pass


class MissingSheetException(XLSImportError):
  """Thrown when there is a missing sheet."""

