# -*- coding: utf-8 -*-

"""Console script for mentormatch."""
import click
from .get_path_from_user import get_path_from_user


@click.command()
@click.option("--version", "-v", is_flag=True)
def main(version):

    if version:
        string_ = "version: " + __version__
        click.echo(string_)
        return

    fdr_excel_path = get_path_from_user()
    click.echo("hello")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
