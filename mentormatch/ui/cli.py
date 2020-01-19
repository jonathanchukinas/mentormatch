# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.exceptions.api as api


@click.command()
def main():
    # --- Welcome -------------------------------------------------------------
    click.clear()
    click.echo(
        "\nWelcome to MentorMatch."
        "\nSelect an excel file to import."
    )

    api.main()

    # --- Outro ---------------------------------------------------------------
    click.echo("\nThank you for using Mentormatch.")
