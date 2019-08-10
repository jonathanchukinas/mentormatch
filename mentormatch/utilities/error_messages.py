# TODO rename this to something more general, like 'logging functions'

import datetime
import logging
from datetime import datetime

def error_rcv_wrong_data(class_name,
                         property_name,
                         expected_value,
                         received_value,
                         converted_to):
    """
    Print error message any time an applicant class receives invalid applicant.

    :param class_name: e.g. ApplicantBiography or ApplicantPreferences
    :param property_name: Input variable that was passed the invalid applicant (e.g. WWIDs, max_mentee_count)
    :param expected_value: str description of what was expected (e.g. 'list of string' or int in [1, 2, 3])
    :param received_value: The invalid argument passed to property_name
    :param converted_to: The value that the invalid argument was converted to.
    :return: N/A
    """
    pass
    # TODO rewrite this so it logs instead of prints.
    #   Also, it should be group-specific. i.e., a mentor doesn't need "wants random mentor"
    # print(f"Error in {class_name}:"
    #       f"\n\tProperty:\t{property_name}"
    #       f"\n\tExpected:\t{expected_value}"
    #       f"\n\tReceived:\t{received_value}"
    #       f"\n\tSaved as:\t{converted_to}")


def log_current_time(prepended_string):
    """Read off some boilerplate to the user."""
    print()
    logging.info(f'{prepended_string}{datetime.now().strftime("%Y-%m-%d %H:%M")}\n')