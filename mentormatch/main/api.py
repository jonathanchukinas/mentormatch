# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.worksheet_data.excel as excel
import mentormatch.main.context_managers as context
from mentormatch.applicants.applicant import Applicant
import mentormatch.matching.matching as matching
import mentormatch.matching.report as report
import mentormatch.main.exceptions as exceptions


def main():

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nPlease select an excel file to import."
    )

    try:
        path = excel.get_path()
        with context.path.set(path):
            worksheet_data = test
        with context.worksheet_data.set(worksheet_data):
            validated_worksheet_data = test2
        with context.worksheet_data.set(validated_worksheet_data):
            mentors = Applicant('mentor')
            mentees = Applicant('mentee')
        with context.mentors.set(mentors), context.mentees.set(mentees):
            matching.preferred_matching()
            matching.random_matching()
            report.print_report()
    except exceptions.MentormatchError as e:
        click.echo(e)

    click.echo(
        "\nThank you for using Mentormatch."
    )


if __name__ == "__main__":
    pass
