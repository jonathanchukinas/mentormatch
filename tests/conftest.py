# --- Standard Library Imports ------------------------------------------------
from pathlib import Path

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------



test_mentormatch_xslx_path = Path(__file__).parent / "files" / "mentormatch_example_applications.xlsx"


@pytest.fixture(scope='session')
def pairs_path():
    return Path(__file__).parent / "files" / "matching_results.toml"


@pytest.fixture(scope='session')
def applications_path():
    return test_mentormatch_xslx_path


@pytest.fixture(scope='session')
def test_files_dir():
    return test_mentormatch_xslx_path.parent


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
