import toml
import pytest
from pathlib import Path


# test_mentormatch_xslx_path = Path(__file__).parent / "files" / "mentormatch_example_applications.xlsx"
test_files_dir = Path(__file__).parent / "files"

#
# @pytest.fixture(scope='session')
# def pairs_path():
#     return Path(__file__).parent / "files" / "matching_results.toml"

#
# @pytest.fixture(scope='session')
# def applications_path():
#     return test_mentormatch_xslx_path
#
#
# @pytest.fixture(scope='session')
# def test_files_dir():
#     return test_mentormatch_xslx_path.parent


@pytest.fixture(scope='function')
def mentors():
    _dict = toml.load(test_files_dir / 'mentors.toml')['mentors']
    return _dict


@pytest.fixture(scope='function')
def mentees():
    _dict = toml.load(test_files_dir / 'mentees.toml')['mentees']
    return _dict
