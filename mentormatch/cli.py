# -*- coding: utf-8 -*-

"""Console script for mentormatch."""
import sys
import click
from mentormatch.get_path import get_path


@click.command()
def main():
    """This application analyzes mentor/ee applications saved in Excel and
    generates the optimal set of mentor/mentee matches.    """
    click.echo("Welcome to the Mentoring Matchmaker!")
    click.echo("Select a file ... any file ...")
    click.echo(get_path())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
