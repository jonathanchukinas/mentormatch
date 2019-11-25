# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import exceptions
from mentormatch.excel import selectfile
from mentormatch.applicants import AllApplicants, Mentee


def main(path=None):

    click.clear()
    click.echo(
        "\nWelcome to Mentormatch."
        "\nSelect an excel file to import."
    )

    # --- Path to excel workbook ----------------------------------------------
    path = selectfile.get_path() if path is None else path

    # --- get applications, build applicants ----------------------------------
    try:
        applicants = AllApplicants(path)
    except exceptions.MentormatchError as e:
        click.echo(e)
        return

    # --- preferred matching --------------------------------------------------
    for mentee in applicants.mentees.awaiting_preferred_match():
        mentee: Mentee
        mentee.assign_to_preferred_mentor()

    # --- random matching -----------------------------------------------------
    # matching.RandomMatching(applicants)
    # TODO reporting?

    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
