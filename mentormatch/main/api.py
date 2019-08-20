# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
# import mentormatch.main.context_managers as context
from mentormatch.applicants.applicant import Applicant
import mentormatch.matching.matching as matching
import mentormatch.matching.report as report
import mentormatch.main.exceptions as exceptions
from mentormatch.applications.applications import get_applications


def main():

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nPlease select an excel file to import."
    )

    try:
        applications = get_applications()
        applicants = get_applicants(applications)
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
