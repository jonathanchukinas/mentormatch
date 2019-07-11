# -*- coding: utf-8 -*-

"""Console script for mentormatch."""
import click
from .get_path_from_user import get_path_from_user
from .. import __version__

@click.command()
@click.option("--version", "-v", is_flag=True)
def main(version):

    if version:
        string_ = "version: " + __version__
        click.echo(string_)
        return

    fdr_excel_path = get_path_from_user()
    click.echo("hello")
