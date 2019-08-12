# --- Standard Library Imports ------------------------------------------------
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None
import click


def get_path():
    return get_path_from_user()


def get_path_from_user():
    root = tk.Tk()
    root.withdraw()
    file_path = Path(filedialog.askopenfilename())
    return str(file_path)


if __name__ == "__main__":
    pass


def importexcel(reuse, new):
    if reuse and not new:
        path = get_last_path()
    elif not reuse and new:
        path = get_path_from_user()
    else:
        path = get_new_or_existing_path_from_user()
    add_path_to_db(path)
    # TODO this is where all the rest of the magic happens.
    click.echo(f"Path: {path}")