"""The Worksheet class abstracts an Excel worksheet, capturing e.g. its header
row number, headers, data, etc"""

# --- Standard Library Imports ------------------------------------------------
import pathlib

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
import xlrd

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main.exceptions import MentormatchError
from mentormatch.get_from_excel.header_row import find_header_row


class Worksheet:

    def __init__(self, excel_path, excel_sheet_name, header_row=1, converters=None):
        try:
            self.df = pd.read_excel(
                io=excel_path,
                sheet_name=excel_sheet_name,
                header=header_row-1,
                converters=converters,
                usecols=converters.keys() if converters else None,
            )
        except FileNotFoundError:
            raise MentormatchError(f'<{excel_path}> not valid file.')
        except xlrd.biffh.XLRDError:
            raise MentormatchError(f"<{excel_sheet_name}> sheet not found")
        # TODO handle exceptions for missing field?
        self.path = excel_path
        self.sheetname = excel_sheet_name
        self.header_row = header_row

    def add_row_column(self):
        row_count = len(self.df.index)
        rows = range(self.header_row, self.header_row + row_count)
        self.df['row'] = rows

    def remove_dups(self):
        """If any wwid is duplicated, keep only the first."""
        # TODO - implement
        #   Warn user about the rows that get ignored
        pass

    def error_check(self):
        # TODO - implement
        #   raise MMError for "deal breakers"
        #   Show warnings for all other "errors"
        pass


if __name__ == '__main__':
    pass
    # path = pathlib.Path(__file__).parent.parent.parent/'test_rtm.xlsx'
    # sheet_name = 'pandas_experiment'
    # headers = 'hello good bye'.split()
    # try:
    #     header_row = find_header_row(path, sheet_name, headers)
    #     df = get_df(path, sheet_name, header_row)
    #     print(df)
    # except MentormatchError as e:
    #     print(e)
