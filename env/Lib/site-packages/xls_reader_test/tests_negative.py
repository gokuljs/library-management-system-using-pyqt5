# -*- coding: utf-8 -*-

# pylint: disable=missing-docstring,invalid-name

import pathlib
import unittest

from xls_reader import *
from xls_reader.exceptions import MissingSheetException

from . import bindings


PARENT_DIR = pathlib.Path(__file__).parent.absolute()  # pylint: disable=no-member

EXAMPLE_FILES = PARENT_DIR / "example_files"


class SheetTestCase(unittest.TestCase):

  FILE_NAME = 'examples_invalid.xlsx'
  SHEET_NAME = None
  EXPECTED_EXCEPTION = None

  def setUp(self):
    if self.SHEET_NAME is None:
      raise unittest.SkipTest()
    self.file_path = EXAMPLE_FILES / self.FILE_NAME
    self.importer = bindings.ExampleDataImporter()

  def test_sheet(self):
    try:
      list(self.importer.read_file(str(self.file_path), self.SHEET_NAME))
    except XLSImportError as e:
      print(repr(e))
      self.assertEqual(type(e), type(self.EXPECTED_EXCEPTION))
      self.assertEqual(e.message, self.EXPECTED_EXCEPTION.message)
      self.assertEqual(e.row, self.EXPECTED_EXCEPTION.row)
      self.assertEqual(e.column, self.EXPECTED_EXCEPTION.column)
      self.assertEqual(e.column_enum, self.EXPECTED_EXCEPTION.column_enum)


class TestUnknownSheet(SheetTestCase):
  FILE_NAME = 'examples_missing_sheet.xlsx'
  SHEET_NAME = 'no such sheet'
  EXPECTED_EXCEPTION = MissingSheetException(
    message="No such sheet no such sheet. Available sheets: "
            "['simple_sheet', 'different_order', 'empty headers and columns', "
            "'missing not required column', 'internal header', 'empty rows']"
  )


class TestMissingReq(SheetTestCase):
  SHEET_NAME = 'missing required column'
  EXPECTED_EXCEPTION = XLSImportError(
    message='Missing required column DataColumns.NAME.'
  )


class TestDuplicateColumn(SheetTestCase):
  SHEET_NAME = 'duplicate column'
  EXPECTED_EXCEPTION = InvalidHeaderFormat(
    message="Duplicate column DataColumns.NAME",
  )


class InternalHeaderWrongOrder(SheetTestCase):
  SHEET_NAME = 'internal header wrong order'
  EXPECTED_EXCEPTION = XLSImportError(
    message="There was a header in the middle of the document, and it wasn't matching "
            "the main header at the top of the document. Please validate if columns "
            "match in both headers and remove one that is lower in the XLS.",
    row=4
  )


class InternalHeaderIntsInHeader(SheetTestCase):
  SHEET_NAME = 'internal header ints in header'
  EXPECTED_EXCEPTION = XLSImportError(
    message='All columns should be strings in header rows,',
    row=4
  )


class InvalidValueInColumn(SheetTestCase):
  SHEET_NAME = 'invalid value in column'
  EXPECTED_EXCEPTION = ColumnReadException(
    message="Cell value is of unexpected type <class 'int'> (value: 1)",
    row=1,
    column='A',
    column_enum=bindings.DataColumns.NAME
  )


class InvalidValueInColumn2(SheetTestCase):
  SHEET_NAME = 'invalid value in column 2'
  EXPECTED_EXCEPTION = ColumnReadException(
    message="Invalid value in yes/no column nah",
    row=2,
    column='E',
    column_enum=bindings.DataColumns.ACTIVE
  )


class EmptyRows(SheetTestCase):
  SHEET_NAME = "extra column"
  EXPECTED_EXCEPTION = UnknownColumnError(
    message="extra column"
  )


