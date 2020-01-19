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
    root = tk.Tk()  # pragma: no cover
    root.withdraw()  # pragma: no cover
    path = Path(filedialog.askopenfilename())  # pragma: no cover
    return path  # pragma: no cover
