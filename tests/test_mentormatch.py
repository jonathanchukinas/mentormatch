from mentormatch.exceptions.api import main
import pytest
import toml
from mentormatch.applicant import AllApplicants
from mentormatch.exceptions.exceptions import MentormatchError
from contextlib import contextmanager
from pytest import raises


@pytest.fixture(scope='session')
def run_api(applications_path):
    main(applications_path)


@pytest.mark.usefixtures("run_api")
def test_pairs(pairs_path):
    pairs = toml.load(pairs_path)['pairs']
    pairs = {
        int(key): value
        for key, value in pairs.items()
    }
    assert 432198765 in pairs[234567891]
    assert 765432198 in pairs[456789123]


@contextmanager
def does_not_raise():
    yield


@pytest.mark.parametrize("filename,callable_,expectation", [
    pytest.param('missing_worksheet.xlsx', AllApplicants, raises(MentormatchError)),
    pytest.param('wrong_row.xlsx', AllApplicants, raises(MentormatchError)),
    pytest.param('wrong_row.xlsx', main, does_not_raise()),
    # pytest.param('missing_favor_ws.xlsx', main, raises(MentormatchError)),  # TODO this isn't working...
])
def test_exceptions(filename, callable_, test_files_dir, expectation):
    test_file_path = test_files_dir / filename
    with expectation:
        callable_(test_file_path)
