"""The Worksheet class abstracts an Excel worksheet, capturing e.g. its header
row number, headers, data, etc"""

# --- Standard Library Imports ------------------------------------------------
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

# --- Third Party Imports -----------------------------------------------------
import click
import openpyxl

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import config
from mentormatch.worksheet import header_row as header


def get_path():
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())
    return path


def get_workbook(path):
    # TODO handle exceptions for bad paths
    return openpyxl.load_workbook(path)


def get_worksheet():
    return None



class Worksheet:



        if find_header_row and converters:
            header_row = header.find_header_row(excel_path, excel_sheet_name, converters.keys())

        # --- raise exceptions for missing file, worksheet, or headers --------
        # --- print warnings for extra headers --------------------------------
        try:
            actual_cols = pd.read_excel(
                io=excel_path,
                sheet_name=excel_sheet_name,
                header=header_row-1,
                nrows=0,
            ).columns
        except FileNotFoundError:
            raise config.MentormatchError(f'<{excel_path}> not valid file.')
        except xlrd.biffh.XLRDError:
            raise config.MentormatchError(f"<{excel_sheet_name}> sheet not found")
        if converters is not None:
            expected_cols = converters.keys()
            missing_cols = [col for col in expected_cols if col not in actual_cols]
            if missing_cols:
                error_txt = f"\n{excel_sheet_name} sheet is missing one or columns:\n{missing_cols}"
                raise config.MissingHeaderError(error_txt)
            extra_columns = [col for col in actual_cols if col not in expected_cols]
            if extra_columns:
                click.echo(f'\nWARNING: unneeded columns found on {excel_sheet_name} sheet:\n{extra_columns}')

        # --- Import excel info dataframe -------------------------------------
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
        self.group = excel_sheet_name if group is None else group
        self.year = year

        if autosetup:
            self.add_row_column()
            self.drop_dups()
            self.error_check()
            self.reset_index()

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

    def reset_index(self):
        self.df = self.df.reset_index(drop=True)

    def error_check(self):
        # TODO - implement
        #   raise MMError for "deal breakers"
        #   Show warnings for all other "errors"
        pass


if __name__ == '__main__':
    pass


