# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.matching.matching as matching
import mentormatch.matching.report as report
import mentormatch.main.exceptions as exceptions
from mentormatch.applications.applications import get_applications
from mentormatch.worksheet.worksheet import Worksheet
from mentormatch.main import config
from mentormatch.worksheet import schema


def main():

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nPlease select an excel file to import."
    )

    try:
        path = 'todo'  # TODO
        worksheets = dict()
        for group in config.groups:
            worksheets[group] = Worksheet(
                excel_path=path,
                excel_sheet_name=group,
                converters=schema.converters[group],
                find_header_row=True,
            )


        # applications = get_applications()
        # applicants = get_applicants(applications)
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
