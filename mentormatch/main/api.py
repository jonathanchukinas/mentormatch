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
    pass
