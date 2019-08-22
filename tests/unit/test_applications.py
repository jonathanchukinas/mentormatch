import mentormatch.applications.applications as applications
from mentormatch.main.exceptions import MentormatchError
from pathlib import Path


def test_get_workbook(test_path):
    get_wb = applications.get_workbook

    # --- No path == error ----------------------------------------------------
    error_thrown = False
    try:
        wb = get_wb(Path('.'))
    except MentormatchError:
        error_thrown = True
    assert error_thrown

    # --- Wrong extension -----------------------------------------------------
    error_thrown = False
    try:
        wb = get_wb(Path('test.docx'))
    except MentormatchError:
        error_thrown = True
    assert error_thrown

    # --- Good file -----------------------------------------------------------
    error_thrown = False
    try:
        wb = get_wb(test_path)
    except MentormatchError:
        error_thrown = True
    assert not error_thrown


def test_get_worksheet(test_wb, groups):

    # --- Force an error ------------------------------------------------------
    error_thrown = False
    try:
        ws = applications.get_worksheet(test_wb, 'banana')
    except MentormatchError:
        error_thrown = True
    assert error_thrown

    # --- Read actual sheets --------------------------------------------------
    worksheets = []
    for group in groups:
        ws = applications.get_worksheet(test_wb, group)
        worksheets.append(ws)
    assert len(worksheets) == 2


def test_get_field_names(test_wb):
    ws = test_wb['test_applications']
    field_names = applications.get_field_names(ws)
    assert field_names == 'first_name last_name wwid'.split()


def test_get_field_col_num(test_wb):
    ws = test_wb['test_applications']
    assert applications.get_field_column_number(ws, 'last_name') == 1


def test_missing_dup_fields():
    actual_fields = 'first_name last_name wwid wwid'.split()
    reqd_fields = 'first_name last_name wwid site'
