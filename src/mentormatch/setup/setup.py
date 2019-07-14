import logging
from pathlib import Path

def logging_setup():
    """This keeps track of status messages to the user."""
    # FYI: How to use logging: https://docs.python.org/3.7/howto/logging.html
    logging.basicConfig(format='%(levelname)s: %(message)s', filemode='w', level=logging.INFO)
    # logging_path = path_to_mentoring_applications.parent / 'report.log'


def get_current_year():
    #   Current year. This is used only for determining the priority of one mentee over another.
    #       Each mentee applicant has a history (what years they applied, which years they got a mentor).
    #       Knowing the current year puts that history into context.
    #       It would probably be a good idea to suggest the current year to the user.
    #       They can then override it if they wish.
    #       Which class makes use of the current year?
    logging.info(f'Determining the current year ...')
    current_year = 2020  # input("Input current year: ")
    logging.info(f'Current Year = {current_year}\n')
    # TODO give user choice for entering the Mentoring Program Year
    # TODO make sure `current year` is actually needed. It may not.
    return current_year


def get_data_path():
    # TODO give user choice for entering path to raw applicant.
    logging.info('Getting path to applicant applicant stored in excel ...')
    path_to_mentoring_applications = Path(__file__).parent.parent.parent / 'data' / 'private' / 'applications.xlsx'
    logging.info(f'Path = {path_to_mentoring_applications}\n')
    return path_to_mentoring_applications


if __name__ == "__main__":
    logging_setup()
    get_current_year()
    get_data_path()
