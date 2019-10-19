# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants.applicants import Applicants
import mentormatch.main.exceptions as exceptions
from mentormatch.worksheet.worksheet import Worksheet
from mentormatch.main import config
from mentormatch.worksheet import schema
from mentormatch.worksheet import get_path


def main(path=None):

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nSelect an excel file to import."
    )

    if path is None:
        path = get_path.get_path()
    try:
        # --- import worksheets -----------------------------------------------
        worksheets = {
            group: Worksheet(
                excel_path=path,
                excel_sheet_name=group,
                converters=schema.converters[group],
                find_header_row=True,
                autosetup=True,
            )
            for group in config.groups
        }
        for ws in worksheets.values():
            ws: Worksheet
            ws.add_row_column()
            ws.drop_dups()

        # --- create applicants -----------------------------------------------
        applicants = {ws.group: Applicants(ws) for ws in worksheets}
        # with context.mentors.set(mentors), context.mentees.set(mentees):
        #     matching.preferred_matching()
        #     matching.random_matching()
        #     report.print_report()
    except exceptions.MentormatchError as e:
        click.echo(e)

    click.echo(
        "\nThank you for using Mentormatch."
    )


if __name__ == "__main__":
    pass
