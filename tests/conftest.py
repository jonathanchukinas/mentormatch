from pathlib import Path
import pytest
import openpyxl


test_mentormatch_xslx_path = Path(__file__).parent / "test_mentormatch.xlsx"


@pytest.fixture(scope='session')
def test_path():
    return test_mentormatch_xslx_path


@pytest.fixture(scope='session')
def test_wb(test_path):
    return openpyxl.load_workbook(test_path)


@pytest.fixture(scope='session')
def groups():
    return 'mentors mentees'.split()


# @pytest.fixture(scope='session')
# def test_ws(test_wb):
#
