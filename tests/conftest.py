import toml
import pytest
from pathlib import Path
from .random_applicant_generator import RandomApplicantGenerator
from datetime import datetime


_test_files_dir = Path(__file__).parent / "files"
mentor_count =10
mentee_count = 2 * mentor_count
now = datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope='function')
def mentors():
    _dict = toml.load(_test_files_dir / 'mentors.toml')['mentors']
    return _dict


@pytest.fixture(scope='function')
def mentees():
    _dict = toml.load(_test_files_dir / 'mentees.toml')['mentees']
    return _dict


# TODO make sure the output dictionaries have the right tense: mentor vs. mentors


@pytest.fixture(scope='function')
def lots_of_applicants():
    applicant_generator = RandomApplicantGenerator()
    applicant_generator.build_mentors(mentor_count)
    applicant_generator.build_mentees(mentee_count)
    return applicant_generator.applicants_dicts


@pytest.fixture(scope='function')
def three_perfect_applicants():
    applicants = toml.load(_test_files_dir / 'perfect_matches.toml')
    return applicants


@pytest.fixture(scope='session')
def test_files_dir():
    return _test_files_dir


@pytest.fixture(scope='function')
def home_dir():
    path = Path.home() / '.mentormatch' / f'mentormatch_{now}'
    path.mkdir()
    return path
