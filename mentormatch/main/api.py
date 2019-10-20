# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.import_worksheet.excel_workbook
from mentormatch import applicant
from mentormatch import worksheet
from mentormatch import matching
from mentormatch import config
from mentormatch.import_worksheet import database
from mentormatch.import_worksheet import excel_workbook


def main(excel_path=None):

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nSelect an excel file to import."
    )

    # --- Paths: excel workbook -----------------------------------------------
    if excel_path is None:
        excel_path = excel_workbook.get_path()

    try:
        # --- Import excel into db --------------------------------------------
        db = database.get_clean_db()
        with excel_workbook.get_workbook(excel_path) as workbook:
            for group in config.groups:
                database.import_worksheet_to_db(
                    workbook=workbook,
                    excel_sheet_name=group,
                    database=db,
                    find_header_row=True,
                    autosetup=True,
                )

        # --- create applicants -----------------------------------------------
        applicants = {group: applicant.Applicants(db, group) for group in config.groups}

        # --- matching --------------------------------------------------------
        # matching.PreferredMatching(applicants)
        # matching.RandomMatching(applicants)
        # TODO reporting
    except config.MentormatchError as e:
        click.echo(e)

    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
