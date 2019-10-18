"""The Worksheet class abstracts an Excel worksheet, capturing e.g. its header
row number, headers, data, etc"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
import xlrd
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import exceptions
from mentormatch.worksheet.header_row import find_header_row


class Worksheet:

    def __init__(self, excel_path, excel_sheet_name, header_row=1, converters=None, find_header_row=False):

        # --- raise exceptions for missing file, worksheet, or headers --------
        try:
            actual_cols = pd.read_excel(
                io=excel_path,
                sheet_name=excel_sheet_name,
                header=header_row-1,
                nrows=0,
            ).columns
        except FileNotFoundError:
            raise exceptions.MentormatchError(f'<{excel_path}> not valid file.')
        except xlrd.biffh.XLRDError:
            raise exceptions.MentormatchError(f"<{excel_sheet_name}> sheet not found")
        if converters is not None:
            expected_cols = converters.keys()
            missing_cols = [col for col in expected_cols if col not in actual_cols]
            if missing_cols:
                error_txt = f"{excel_sheet_name} sheet is missing one or columns:\n{missing_cols}"
                raise exceptions.MissingHeaderError(error_txt)

        # --- Import worksheet info dataframe ---------------------------------
        self.df = pd.read_excel(
            io=excel_path,
            sheet_name=excel_sheet_name,
            header=header_row-1,
            converters=converters,
            usecols=converters.keys() if converters else None,
        )
        self.path = excel_path
        self.sheetname = excel_sheet_name
        self.header_row = header_row

    def add_row_column(self):
        row_count = len(self.df.index)
        first_data_row = self.header_row + 1
        rows = range(first_data_row, row_count + first_data_row)
        self.df['row'] = rows

    def drop_dups(self):
        """If any wwid is duplicated, keep only the first."""
        if 'row' not in self.df:
            self.add_row_column()
        rows_initial = list(self.df['row'])
        self.df.drop_duplicates(subset='wwid', keep='first', inplace=True)
        rows_after = list(self.df['row'])
        rows_removed = [row for row in rows_initial if row not in rows_after]
        if rows_removed:
            click.echo("\nIf a wwid is duplicated, only the first instance is kept.")
            click.echo(f'The following rows from the {self.sheetname} workbook were ignored as a result:')
            click.echo(rows_removed)
            return rows_removed
        return []

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
