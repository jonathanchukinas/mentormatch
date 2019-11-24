"""Provides user with file select dialog."""

# --- Standard Library Imports ------------------------------------------------
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


def get_path():
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())
    return path


if __name__ == '__main__':
    pass
