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
