"""These higher-order functions are called to generate a dataframe from an
excel worksheet"""

# --- Standard Library Imports ------------------------------------------------
import pathlib

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
import xlrd

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main.exceptions import MentormatchError
from mentormatch.get_from_excel.header_row import find_header_row


def get_df(excel_path, excel_sheet_name, header_row=1, converters=None):  # , index=None):
    # TODO - for each dtype dict key, remove key from converters
    try:
        df = pd.read_excel(
            io=excel_path,
            sheet_name=excel_sheet_name,
            header=header_row-1,
            # dtype=dtype,
            converters=converters,
            usecols=converters.keys() if converters else None,
            # index=index,
        )
    except FileNotFoundError:
        raise MentormatchError(f'<{excel_path}> not valid file.')
    except xlrd.biffh.XLRDError:
        raise MentormatchError(f"<{excel_sheet_name}> sheet not found")

    # TODO
    #   Quality-check data
    #       Remove duplicate wwids, report this to user. highlight cells in workbook copy.
    #       Highlight rows that have errors. Save copy. Throw MM error, catch, and print message
    #   set index equal to row numbers
    #

    return df


def set_index_equal_to_row_num(df, header_row):
    return df


if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.parent.parent/'test_rtm.xlsx'
    sheet_name = 'pandas_experiment'
    headers = 'hello good bye'.split()
    try:
        header_row = find_header_row(path, sheet_name, headers)
        df = get_df(path, sheet_name, header_row)
        print(df)
    except MentormatchError as e:
        print(e)



