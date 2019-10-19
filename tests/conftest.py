from pathlib import Path
import pytest
import openpyxl
from mentormatch.worksheet.worksheet import Worksheet


test_mentormatch_xslx_path = Path(__file__).parent / "test_mentormatch.xlsx"


@pytest.fixture(scope='session')
def fixture_path():
    return test_mentormatch_xslx_path


@pytest.fixture(scope='session')
def fixture_get_ws():
    def get_ws(worksheet_name: str, autosetup=False):
        return Worksheet(test_mentormatch_xslx_path, worksheet_name, autosetup=autosetup)
    return get_ws
