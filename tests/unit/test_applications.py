import mentormatch.applications.applications as applications
import openpyxl
from mentormatch.main.exceptions import MentormatchError


def test_get_worksheets(test_path):
    wb = openpyxl.load_workbook(test_path)

    # --- Force an error ------------------------------------------------------
    error_thrown = False
    try:
        worksheets = applications.get_worksheets(wb, 'hello bye'.split())
    except MentormatchError:
        error_thrown = True
    assert error_thrown

    # --- Read actual sheets --------------------------------------------------
    worksheets = applications.get_worksheets(wb, 'mentors mentees'.split())
    assert len(worksheets) == 2
