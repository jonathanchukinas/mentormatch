# -*- coding: utf-8 -*-

"""Console script for mentormatch."""
import click
import mentormatch


@click.command()
def mentormatch_cli():
    # fdr_excel_path = get_path_from_user()
    click.echo("calling mentormatch_cli")
    mentormatch.lumberjack()
