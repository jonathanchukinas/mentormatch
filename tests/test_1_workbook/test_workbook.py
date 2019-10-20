import mentormatch.import_worksheet.excel_workbook as workbook
from mentormatch import config


def test_get_path_not_exist(fixture_path):
    missing_path = fixture_path.parent / 'missing_file.xlsx'
    try:
        workbook.get_workbook(missing_path)
    except config.MentormatchError:
        return
    assert False


def test_get_path_extension_not_valid(fixture_path):
    missing_path = fixture_path.parent / 'not_excel.docx'
    try:
        workbook.get_workbook(missing_path)
    except config.MentormatchError:
        return
    assert False


def test_get_missing_worksheet(fixture_path):
    ws_name = 'missing_worksheet'
    wb = workbook.get_workbook(fixture_path)
    try:
        workbook.get_worksheet(wb, ws_name)
    except config.MentormatchError:
        return
    assert False
