# --- Standard Library Imports ------------------------------------------------
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

# --- Third Party Imports -----------------------------------------------------
import openpyxl
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main.exceptions import MentormatchError


def get_applications():

    groups = 'mentors mentees'.split()
    path = get_path()
    wb = get_workbook(path)
    worksheets = get_worksheets(wb, groups)

    """Pseudocode

    Get list of req'd fields
    Check applications against this list.
    Any fields are missing or duplicated. Throw error summarizing any misses or dups.
    For each req'd field, check all values against

    """


def get_path():

    # --- User selects path ---------------------------------------------------
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())

    # --- Check that a file was selected --------------------------------------
    if str(path) == '.':
        raise MentormatchError("You didn't select a file")

    # --- Check that file has proper extension --------------------------------
    required_extensions = '.xlsx .xls'.split()
    if path.suffix not in required_extensions:
        msg = f"You selected a file without aproper extension: {required_extensions}"
        raise MentormatchError(msg)

    # --- Finish --------------------------------------------------------------
    click.echo(f"\nThe RTM you selected is {path}")
    return path


def get_workbook(path):
    return openpyxl.load_workbook(filename=str(path), read_only=True, data_only=True)


def get_worksheets(workbook, sheetnames):
    worksheets = dict()
    try:
        for name in sheetnames:
            worksheets[name] = workbook[name]
    except KeyError:
        raise MentormatchError(f'Ensure excel workbook contains worksheets {sheetnames}')
    return worksheets


def get_field_names(worksheet):
    ws = worksheet
    return [ws.cell(1, col).value for col in range(1, ws.max_column + 1)]


if __name__ == '__main__':
    pass
