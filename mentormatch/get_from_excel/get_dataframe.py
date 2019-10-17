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


def get_df(excel_path, excel_sheet_name, header_row=1):
    try:
        return pd.read_excel(
            io=excel_path,
            sheet_name=excel_sheet_name,
            header=header_row-1,
            dtype=object,
        )
    except FileNotFoundError:
        raise MentormatchError(f'<{excel_path}> not valid file.')
    except xlrd.biffh.XLRDError:
        raise MentormatchError(f"<{excel_sheet_name}> sheet not found")


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

