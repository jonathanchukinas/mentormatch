# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import applicant
from mentormatch import worksheet
from mentormatch import matching
from mentormatch import config


def main(path=None):

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nSelect an excel file to import."
    )

    if path is None:
        path = worksheet.get_path()
    try:
        # --- import worksheets -----------------------------------------------
        worksheets = dict()
        for group in config.groups:
            ws = worksheet.Worksheet(
                excel_path=path,
                excel_sheet_name=group,
                converters=worksheet.converters[group],
                find_header_row=True,
                autosetup=True,
            )
            worksheets[group] = ws
        for ws in worksheets.values():
            ws: worksheet.Worksheet
            ws.add_row_column()
            ws.drop_dups()

        # --- create applicant -----------------------------------------------
        applicants = {group: applicant.Applicants(worksheets[group]) for group in config.groups}

        # --- matching --------------------------------------------------------
        # matching.PreferredMatching(applicants)
        # matching.RandomMatching(applicants)
        # TODO reporting
    except config.MentormatchError as e:
        click.echo(e)

    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
