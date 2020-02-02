from mentormatch.exceptions import exceptions
import click
from mentormatch.api.app.app_main import main
from mentormatch.exporter import ExporterFactory
from pathlib import Path
from datetime import datetime


@click.command()
def main():

    # --- Welcome -------------------------------------------------------------
    click.clear()
    click.echo(
        "\nWelcome to MentorMatch."
        "\nSelect an excel file to import."
    )

    # --- import applications -------------------------------------------------
    mentors = []
    mentees = []
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path.home() / '.mentormatch' / f'mentormatch_{now}'

    # --- run app -------------------------------------------------------------
    try:
        results = main()
    except exceptions.MentormatchError as e:
        click.echo(e)
        return

    # --- export results ------------------------------------------------------
    exporter = ExporterFactory(results_dir).get_exporter()
    exporter.export_inputs(mentors, mentees)
    exporter.export_results(results=results)

    # --- Outro ---------------------------------------------------------------
    click.echo("\n\n\nThank you for using Mentormatch.")
    click.echo("You can find your results here:")
    click.echo(results_dir)
