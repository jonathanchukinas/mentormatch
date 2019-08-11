# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.excel_data_handling.excel as excel
import mentormatch.main.context_managers as context
import mentormatch.applicants.mentor as mentor
import mentormatch.applicants.mentee as mentee
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
            mentors = mentor.Mentors()
            mentees = mentee.Mentees()
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
