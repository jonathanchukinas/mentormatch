# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.excel.selectfile
from mentormatch import applicant
from mentormatch import worksheet
from mentormatch import matching
from mentormatch import config
from mentormatch.excel import database
from mentormatch.excel import selectfile
from mentormatch.excel import fieldschema
from mentormatch.excel.fieldschema import fieldschema


def main(path=None):

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nSelect an excel file to import."
    )

    # --- Path to excel workbook ----------------------------------------------
    path = selectfile.get_path() if path is None else path

    # --- extract tables from excel -------------------------------------------
    applications = {}
    try:
        for group, fieldpattern in fieldschema.items():
            applications[group] = FuzzyTable(
                path=path,
                sheetname=group,
                fields=fieldpattern,
                header_row_seek=True,
                name=group,
                approximate_match=False,
                missingfieldserror_active=True,
            )
    except FuzzyTableError as e:
        click.echo(e)
        return

    # --- Import excel into db --------------------------------------------
    db = database.get_clean_db()
    wb = selectfile.get_workbook(path)
    for group in applications.keys():
        database.import_worksheet_to_db(
            workbook=wb,
            excel_sheet_name=group,
            database=db,
            header=fieldschema.fieldschema[group],
            autosetup=True,
        )

    # --- create applicants -----------------------------------------------
    applicants = {group: applicant.Applicants(db, group) for group in applications.keys()}

    # --- matching --------------------------------------------------------
    # matching.PreferredMatching(applicants)
    # matching.RandomMatching(applicants)
    # TODO reporting


    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
