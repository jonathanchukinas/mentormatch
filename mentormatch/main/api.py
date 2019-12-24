# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import click
import toml

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import exceptions
from mentormatch.excel import selectfile
from mentormatch.applicants import AllApplicants
from mentormatch.matching.matching import Matching


def main(path=None):

    # --- Welcome -------------------------------------------------------------
    click.clear()
    click.echo(
        "\nWelcome to MentorMatch."
        "\nSelect an excel file to import."
    )

    # --- Path to excel workbook ----------------------------------------------
    path = selectfile.get_path() if path is None else path

    # --- get applications, build applicants ----------------------------------
    try:
        applicants = AllApplicants(path)  # TODO db: initialize with new, blank resume
    except exceptions.MentormatchError as e:
        click.echo(e)
        return

    # --- preferred matching --------------------------------------------------
    matching_algorithm = Matching(applicants)
    matching_algorithm.preferred_matching()
    matching_algorithm.random_matching()

    # --- print results -------------------------------------------------------
    applicants_dict = {}  # keys: mentors/ees
    for groupname, applicants in applicants.items():
        group_dict = {
            str(applicant): dict(applicant)
            for applicant in applicants.values()
        }
        applicants_dict[groupname] = group_dict
    applicants_tomlstring = toml.dumps(applicants_dict)
    toml_path = path.parent / "matching_results.toml"
    with open(toml_path, "w") as f:
        f.write(applicants_tomlstring)

    # --- Outro ---------------------------------------------------------------
    click.echo("\nThank you for using Mentormatch.")


if __name__ == "__main__":
    pass
