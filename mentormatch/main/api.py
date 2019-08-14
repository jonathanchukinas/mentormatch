# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.applications.excel as excel
import mentormatch.main.context_managers as context
from mentormatch.applicants.applicant import Applicant
import mentormatch.matching.matching as matching
import mentormatch.matching.report as report
import mentormatch.main.exceptions as exceptions
import mentormatch.applications.worksheet_columns as wc


def main():

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nPlease select an excel file to import."
    )

    try:
        path = excel.get_path()
        with context.path.set(path):
            applications = wc.Applications(
                mentors=wc.Fields("mentors"),
                mentees=wc.Fields("mentors")
            )
        with context.applications.set(applications):
            validated_applications = test2
        with context.applications.set(validated_applications):
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
