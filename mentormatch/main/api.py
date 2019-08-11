# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
import mentormatch.excel_data_handling.excel as excel
import mentormatch.main.context_managers as context
import mentormatch.applicants.mentor as mentor
import mentormatch.applicants.mentee as mentee
import mentormatch.matching.matching as matching
import mentormatch.matching.report as report


def main():
    path = excel.get_path()
    with context.path.set(path):
        mentors = mentor.Mentors()
        mentees = mentee.Mentees()
    with context.mentors.set(mentors), context.mentees.set(mentees):
        matching.preferred_matching()
        matching.random_matching()
        report.print_report()


if __name__ == "__main__":
    pass
