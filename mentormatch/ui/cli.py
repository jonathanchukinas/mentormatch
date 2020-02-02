import click
from mentormatch.api.app.app_main import main as main_api
from mentormatch.importer import ImporterFactory
from mentormatch.exporter import ExporterFactory
from pathlib import Path
from datetime import datetime
from mentormatch.utils import ApplicantType


@click.command()
def main():

    # --- Welcome -------------------------------------------------------------
    click.clear()
    click.echo(
        "\nWelcome to MentorMatch."
        "\nSelect an excel file to import."
    )

    # --- set directory -------------------------------------------------------
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = Path.home() / '.mentormatch' / f'mentormatch_{now}'

    # --- import applications -------------------------------------------------
    importer_factory = ImporterFactory()
    source_path = importer_factory.select_file_dialog()
    applications = importer_factory.get_exceltoml_importer(
        source_path=source_path,
        save_path=save_dir,
    ).execute()
    mentors = applications[ApplicantType.MENTOR]
    mentees = applications[ApplicantType.MENTEE]

    # --- run app -------------------------------------------------------------
    results = main_api(mentors, mentees)

    # --- export results ------------------------------------------------------
    exporter = ExporterFactory(save_dir).get_exporter()
    exporter.export_inputs(mentors, mentees)
    exporter.export_results(results=results)

    # --- Outro ---------------------------------------------------------------
    click.echo("\n\n\nThank you for using Mentormatch.")
    click.echo("You can find your results here:")
    click.echo(save_dir)
