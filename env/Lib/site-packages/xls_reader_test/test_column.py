# coding=utf-8

# pylint: disable=missing-docstring,invalid-name


import datetime
import decimal
import enum
import typing

import pytest


from xls_reader import *


MockCell = typing.NamedTuple(
  "MockCell",
  (
    ("value", typing.Any),
  )
)


def test_column_repr():

  class ExampleColumn(Column):
    TEST = ColumnDescription(
      regex="Name",  # Name is the column header
      reader=StringReader(attr_name="name")
    )

  assert repr(ExampleColumn.TEST) == "Column.TEST"


def test_base_column_reader_constructor():
  assert BaseColumnReader(attr_name="test", expected_types=None).expected_types is None
  assert BaseColumnReader(attr_name="test", expected_types=int).expected_types == (int, )


def test_base_column_pre_checks():
  reader = BaseColumnReader(attr_name="test", required=True, expected_types=None)
  with pytest.raises(ColumnReadException):
    reader.pre_checks(MockCell(None))
  reader = BaseColumnReader(attr_name="test", required=True, expected_types=int)
  with pytest.raises(ColumnReadException):
    reader.pre_checks(MockCell("foo"))


def test_string_reader_expected_types():
  assert StringReader(attr_name="test").expected_types == (str, )
  number_accepting_reader = StringReader(attr_name="test", allow_numbers_as_strings=True)
  assert number_accepting_reader.expected_types == (str, int, float, decimal.Decimal)


def test_integer_reader_int_value():
  reader = IntegerReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell(1)) == 1


def test_integer_reader_str_value():
  reader = IntegerReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell("1")) == 1


def test_integer_reader_nan_value():
  reader = IntegerReader(attr_name="test")
  with pytest.raises(ColumnReadException):
    reader.get_value_from_cell(MockCell("not a number"))


def test_decimal_reader_int_value():
  reader = DecimalReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell(1)) == decimal.Decimal("1.0")


def test_decimal_reader_str_value():
  reader = DecimalReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell("1")) == decimal.Decimal("1.0")


def test_decimal_reader_decimal_value():
  expected = decimal.Decimal("1.0")
  reader = DecimalReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell(expected)) is expected


def test_decimal_reader_nan_value():
  reader = DecimalReader(attr_name="test")
  with pytest.raises(ColumnReadException):
    reader.get_value_from_cell(MockCell("not a number"))


class TestEnum(enum.Enum):
  FOO = 1
  BAR = "BaZ"


def test_enum_column_get_by_name():
  reader = EnumReader(attr_name="test", enum_type=TestEnum)
  assert reader.get_value_from_cell(MockCell("FOO")) == TestEnum.FOO
  assert reader.get_value_from_cell(MockCell("foo")) == TestEnum.FOO
  assert reader.get_value_from_cell(MockCell("BAR")) == TestEnum.BAR
  assert reader.get_value_from_cell(MockCell("bar")) == TestEnum.BAR

  assert reader.get_value_from_cell(MockCell("FoO")) == TestEnum.FOO


def test_enum_column_get_by_value():
  reader = EnumReader(attr_name="test", enum_type=TestEnum)
  assert reader.get_value_from_cell(MockCell(1)) == TestEnum.FOO
  assert reader.get_value_from_cell(MockCell("BAZ")) == TestEnum.BAR
  assert reader.get_value_from_cell(MockCell("baz")) == TestEnum.BAR
  assert reader.get_value_from_cell(MockCell("BaZ")) == TestEnum.BAR


def test_enum_column_invalid_value():
  reader = EnumReader(attr_name="test", enum_type=TestEnum)
  with pytest.raises(ColumnReadException):
    assert reader.get_value_from_cell(MockCell("foobar")) == TestEnum.BAR


def test_date_column():
  reader = DatetimeReader(attr_name="test")
  today = datetime.date.today()
  assert reader.get_value_from_cell(MockCell(today)) == today
  now = datetime.datetime.now()
  assert reader.get_value_from_cell(MockCell(now)) == now


def test_date_column_invalid_value():
  reader = DatetimeReader(attr_name="test")
  with pytest.raises(ColumnReadException):
    reader.get_value_from_cell(MockCell("not a date"))


def test_magic_values_for_date_column():
  magic_values = {
    "done": datetime.datetime.now(),
    "n/a": None
  }

  class MagicDateTimeReader(DatetimeReader):
    @classmethod
    def get_magic_values(cls) -> typing.Mapping[str, datetime.datetime]:
      return magic_values

  reader = MagicDateTimeReader(attr_name="test")
  assert reader.get_value_from_cell(MockCell("done")) == magic_values['done']
  assert reader.get_value_from_cell(MockCell("n/a")) is None


def test_boolean_column():

  reader = BooleanReader(attr_name="foo")
  assert reader.get_value_from_cell(MockCell("1")) is True
  assert reader.get_value_from_cell(MockCell("yes")) is True

  assert reader.get_value_from_cell(MockCell("0")) is False
  assert reader.get_value_from_cell(MockCell("no")) is False


def test_boolean_column_invalid_string():
  reader = BooleanReader(attr_name="foo")
  with pytest.raises(ColumnReadException):
    assert reader.get_value_from_cell(MockCell("not a value"))
