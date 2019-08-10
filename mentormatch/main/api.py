"""
Functions here in api.py mirror those in cli.py
"""
import click
from mentormatch.import_from_excel import (
    get_last_path,
    get_path_from_user,
    get_new_or_existing_path_from_user,
    add_path_to_db
)

# def print_version():
#     string_ = "version: " + __version__
#     click.echo(string_)
#     return


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
