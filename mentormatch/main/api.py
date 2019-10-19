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
        worksheets = {
            group: worksheet.Worksheet(
                excel_path=path,
                excel_sheet_name=group,
                converters=worksheet.schema.converters[group],
                find_header_row=True,
                autosetup=True,
            )
            for group in config.groups
        }
        for ws in worksheets.values():
            ws: worksheet.Worksheet
            ws.add_row_column()
            ws.drop_dups()

        # --- create applicant -----------------------------------------------
        applicants = {ws.group: applicant.Applicants(ws) for ws in worksheets}

        # --- matching --------------------------------------------------------
        matching.PreferredMatching(applicants)
        matching.RandomMatching(applicants)
        #     report.print_report()
    except config.MentormatchError as e:
        click.echo(e)

    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
