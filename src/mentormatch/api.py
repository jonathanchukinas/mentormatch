# from src.mentormatch import __version__
import click
from mentormatch.config import mentormatch_db_connection
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# def print_version():
#     string_ = "version: " + __version__
#     click.echo(string_)
#     return


def get_excel_path():

    with mentormatch_db_connection() as db:

        # --- Are there existing records? -------------------------------------
        records_exist = False
        table = db.table("excel_paths")
        document_count = table.count()
        if document_count > 0:
            records_exist = True

        # --- Get user input --------------------------------------------------
        if records_exist:
            # get last 3 records (or as many as there are)
            #
            pass
        else:
            path = get_excel_path_from_user()
            table.insert({"path": path})

            click.prompt(
                f"The last excel file selected was {path}.\nReuse [r] or select new [n]?"
            )
            user_selection = click.Choice(["r", "n"], case_sensitive=False)
            if user_selection == "r":
                return path
            elif user_selection == "n":
                pass
            else:
                raise ValueError(f"'r' or 'n' was expected.")
        path = get_excel_path_from_user()


def get_excel_path_from_user():
    root = tk.Tk()
    root.withdraw()
    file_path = Path(filedialog.askopenfilename())
    return file_path


if __name__ == "__main__":
    # print("Hello World")
    # print("This is the file you selected:", ge())
    # input("Press Enter to exit: ")

    # --- Confirmation Prompt -------------------------------------------------
    # if click.confirm("This was the last path use: <path>\nWould you like to select a new one instead?"):
    #     click.echo("you said yes!!")
    # else:
    #     click.echo("You said no :(")

    # --- validated string input ----------------------------------------------
    # click.prompt(
    #     f"The last excel file selected was <path>.\n"
    #     f"Reuse [r] or select new [n]?"
    # )
    # user_selection = click.Choice(["r", "n"], case_sensitive=False)
    # if user_selection == "r":
    #     click.echo("you selected r")
    # elif user_selection == "n":
    #     click.echo("you selected n")
    # else:
    #     raise ValueError(f"'r' or 'n' was expected.")

    # --- range of integers ---------------------------------------------------
    # int_ = click.prompt("Gimme an integer between 0 and 5", type=click.IntRange(min=0, max=5))
    # click.echo(f"You selected {int_}")

    # --- list of strings -----------------------------------------------------
    click.echo(
        f"\n--- Options ---\n"
        f"[R]euse the last excel file: <path>\n"
        f"Select a [n]ew file"
    )
    str_ = click.prompt(
        "Make your selection", type=click.Choice(["R", "n"], case_sensitive=False)
    )
    click.echo(f"You selected {str_}")
