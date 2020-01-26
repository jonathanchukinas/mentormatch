from mentormatch.exceptions import exceptions
import click
from mentormatch.api.app.app_main import main


@click.command()
def main():

    # --- Welcome -------------------------------------------------------------
    click.clear()
    click.echo(
        "\nWelcome to MentorMatch."
        "\nSelect an excel file to import."
    )

    # --- run app -------------------------------------------------------------
    try:
        main()
    except exceptions.MentormatchError as e:
        click.echo(e)
        return

    # --- Outro ---------------------------------------------------------------
    click.echo("\nThank you for using Mentormatch.")
