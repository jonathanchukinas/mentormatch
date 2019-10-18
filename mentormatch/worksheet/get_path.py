"""Functions for using the tkinter user interface"""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from tkinter import filedialog
import tkinter as tk

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


def get_path():
    root = tk.Tk()
    root.withdraw()
    path = Path(filedialog.askopenfilename())
    return path
