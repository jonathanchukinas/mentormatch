import toml
import pytest
from pathlib import Path
from .randomly_generated_applicants import randomly_generated_mentors, randomly_generated_mentees

test_files_dir = Path(__file__).parent / "files"
mentor_count = 10
mentee_count = 20


@pytest.fixture(scope='function')
def mentors():
    _dict = toml.load(test_files_dir / 'mentors.toml')['mentors']
    return _dict


@pytest.fixture(scope='function')
def mentees():
    _dict = toml.load(test_files_dir / 'mentees.toml')['mentees']
    return _dict


@pytest.fixture(scope='function')
def lots_of_applicants():
    return {
        'mentors': randomly_generated_mentors(mentor_count),
        'mentees': randomly_generated_mentees(mentee_count),
    }
#
#
# @pytest.fixture(scope='function')
# def mentee_generator():
#     return randomly_generated_mentors(1)


# @pytest.fixture(scope='session')
# def get_wwids():
#     applicant_count = mentor_count + mentee_count
#     multiplier = 10
#
#     return tuple(
#         randrange(1, applicant_count * multiplier)
#         for _ in range(applicant_count)
#     )
