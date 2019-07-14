import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def get_path_from_user():
    root = tk.Tk()
    root.withdraw()
    file_path = Path(filedialog.askopenfilename())
    return file_path


if __name__ == "__main__":
    print("Hello World")
    print("This is the file you selected:", get_path())
    input("Press Enter to exit: ")