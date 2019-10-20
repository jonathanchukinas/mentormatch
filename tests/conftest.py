# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
# from mentormatch import worksheet
from mentormatch import applicant
from mentormatch import config


test_mentormatch_xslx_path = Path(__file__).parent / "test_mentormatch.xlsx"


@pytest.fixture(scope='session')
def fixture_path():
    return test_mentormatch_xslx_path


# def get_ws(worksheet_name: str, autosetup=False):
#     return worksheet.Worksheet(test_mentormatch_xslx_path, worksheet_name, autosetup=autosetup)
#
#
# @pytest.fixture(scope='session')
# def fixture_get_ws():
#     return get_ws


# @pytest.fixture(scope='function')
# def fixture_applicants():
#     applicants = dict()
#     for group in config.groups:
#         ws = get_ws(group, autosetup=True)
#         applicants[group] = applicant.Applicants(ws)
#     return applicants
