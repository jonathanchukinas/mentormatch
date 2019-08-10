from .config import mentormatch_db_connection
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import click
from tinydb import Query, where


def get_new_or_existing_path_from_user():
    options = get_last_n_paths(3)
    options_count = len(options)
    if options_count == 0:
        return get_path_from_user()
    options = ["Select a new excel file"] + options
    for index, option in enumerate(options):
        click.echo(f"[{index}] - {option}")
    choice = click.prompt(
        "Select from the above options",
        type=click.IntRange(min=0, max=(options_count + 1)),
    )
    if choice == 0:
        return get_path_from_user()
    else:
        return options[choice]


def get_path_from_user():
    root = tk.Tk()
    root.withdraw()
    file_path = Path(filedialog.askopenfilename())
    return str(file_path)


def get_last_path():
    list_with_one_path = get_last_n_paths(1)
    if len(list_with_one_path) == 0:
        return ""
    else:
        return list_with_one_path[0]


def get_last_n_paths(path_count):
    if not isinstance(path_count, int):
        raise TypeError("path_count must be an integer")
    if path_count < 1:
        raise ValueError("path_count must be greater than zero")
    with mentormatch_db_connection() as db:
        ExcelPath = Query()
        # TODO fix the following:
        paths = db.table("excel_paths").all()  # search(ExcelPath.path.exists)
    paths = [path["path"] for path in paths]
    return paths[: -(path_count + 1): -1]


def add_path_to_db(path):
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    with mentormatch_db_connection() as db:
        paths = db.table("excel_paths")
        paths.remove(where("path") == path)
        paths.insert({"path": path})


if __name__ == "__main__":
    banana = [1, 2, 3]
    grape = ["hi"] + banana
    print(grape)

    # --- exception testing ---------------------------------------------------
