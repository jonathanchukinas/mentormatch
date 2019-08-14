# --- Standard Library Imports ------------------------------------------------
import tkinter as tk
from pathlib import Path
from tkinter import filedialog


# --- Third Party Imports -----------------------------------------------------
import openpyxl
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main.exceptions import MentormatchError
from mentormatch.applications.schema import get_schema


# main callable
def get_applications():

    groups = 'mentors mentees'.split()
    path = get_path()
    wb = get_workbook(path)
    for group in groups:
        ws = get_worksheet(wb, group)
        required_fields = get_schema(group)
        required_field_names = set(field.name for field in required_fields)
        actual_field_names = set(get_field_names(ws))
        # TODO Throw error if missing and dup fields
        validated_fields = dict()
        for field in required_fields:
            name = field.name
            validated_fields[name] = get_validated_values(ws, name, field.val_func)


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


def get_worksheet(workbook, sheetname):
    worksheets = dict()
    try:
        return workbook[sheetname]
    except KeyError:
        raise MentormatchError(f'Ensure excel workbook contains worksheet {sheetname}')


def get_field_names(worksheet):
    ws = worksheet
    return [ws.cell(1, col).value for col in range(1, ws.max_column + 1)]


def get_validated_values(worksheet, field_name, validation_function):
    values = []
    col = get_field_column_number(worksheet, field_name)
    for row in range(2, worksheet.max_row+1):
        orig_value = worksheet.cell(row, col).value
        validated_value = validation_function(orig_value)
        values.append(validated_value)
    return values


def get_field_column_number(worksheet, field_name):
    for col_number in range(1, worksheet.max_column + 1):
        if worksheet.cell(1, col_number).value == field_name:
            return col_number
    raise ValueError(f'{field_name} not found in {worksheet}')

if __name__ == '__main__':
    pass
