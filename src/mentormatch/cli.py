# -*- coding: utf-8 -*-

"""Console script for mentormatch."""
import click
import mentormatch


@click.group()
@click.option("--version")
def mentormatch_cli(version):
    # fdr_excel_path = get_path_from_user()
    click.echo("calling mentormatch_cli")


@mentormatch_cli.command()
def importexcel():
    click.echo("execute `importexcel`")
    matchmaker.get_excel_path()
    # TODO pseudocode
    #   Check that file exists. throw error if not.
    #   Check if file contains mentors and mentees. Throw error if not
    #   Check each spreadsheet for its fields. For each spreadsheet:
    #       throw error if a field is missing (make sure to list all the missing ones)
    #       throw error if field is duplicated (list all the dups. Use a counter?)
    #       throw warning if extra fields (list all extras)
    #   For each field
    #       check for correctness
    #       use counter and report on either all or some of the values (so user can see what was entered)
    #       throw errors where necessary
    #       If all correct, report on random assortment with counts
    #       If incorrect, show some of all of the failures. Throw an error
    #   purge db tables mentors and mentees
    #   add mentors and mentees to db
    #   report successful add


