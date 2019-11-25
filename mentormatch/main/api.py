# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import matching
from mentormatch.db import database
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

    # --- initialize db -------------------------------------------------------
    db = database.get_clean_db()

    # --- get applications from excel -----------------------------------------
    for group_name, fieldpatterns in fieldschema.items():
        try:
            applications = FuzzyTable(
                path=path,
                sheetname=group_name,
                fields=fieldpatterns,
                header_row_seek=True,
                name=group_name,
                approximate_match=False,
                missingfieldserror_active=True,
            )
        except FuzzyTableError as e:
            click.echo(e)
            return

    # --- add applications to db ----------------------------------------------
        records = applications.records  # list of dicts, each representing an applicant
        database.add_group_to_db(group_name=group_name, records=records, database=db)

    # --- create applicants -----------------------------------------------
    mentors = Mentors(db)
    mentees = Mentees(db)x

    # --- preferred matching --------------------------------------------------
    mentees.
    for mentee in mentees.awaiting_preferred_match:
        mentee.attempt_to_assign_preferred_mentor()
    # matching.RandomMatching(applicants)
    # TODO reporting

    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
