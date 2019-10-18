# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
import pytest
import pandas as pd
nan = pd.np.nan

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.get_from_excel import header_row, worksheet, schema


def empty_converter(value):
    return value


converters = {
    'wwid': empty_converter,
    'first_name': empty_converter,
}


def test_names(test_path):

    # --- get dataframe -------------------------------------------------------
    df = worksheet.get_df(test_path, 'test_index_names', converters=converters)
    print()
    print(df)

    # --- compare -------------------------------------------------------------
    expected_headers = set(converters.keys())
    actual_headers = set(df.columns)
    assert actual_headers == expected_headers


# def test_index(test_path):
#
#     # --- get dataframe -------------------------------------------------------
#     df = get_dataframe.get_df(test_path, 'test_index_names', converters=converters, index='wwid')
#     print()
#     print(df)
#
#     # --- compare -------------------------------------------------------------
#     expected_headers = set(converters.keys())
#     actual_headers = set(df.columns)
#     assert actual_headers == expected_headers
