# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,invalid-name

import enum
import re

from xls_reader import *


class Category(enum.Enum):

  OFFICE = 0
  WAREHOUSE = 1


class DataColumns(Column):

  # A string column
  NAME = ColumnDescription(
    regex="Name",  # Name is the column header
    reader=StringReader(attr_name="name")
  )

  PRICE_CENTS = ColumnDescription(
    regex="Price",
    reader=DecimalReader(attr_name="price")
  )

  LOCATION = ColumnDescription(
    regex=re.compile(r"\s*Loc.*", re.IGNORECASE),
    reader=EnumReader(attr_name="location", enum_type=Category)
  )

  DESCRIPTION = ColumnDescription(
    regex="description", reader=StringReader(attr_name="description", required=False)
  )

  ACTIVE = ColumnDescription(
    regex="active", reader=BooleanReader(required=False, default=True, attr_name="active")
  )

  DATE_ADDED = ColumnDescription(
    regex="date", reader=DatetimeReader(required=True, attr_name="date_added")
  )


class ExampleDataImporter(DataImporter):
  @classmethod
  def get_column_enum(cls) -> Column:
    return DataColumns
