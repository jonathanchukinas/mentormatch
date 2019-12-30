from mentormatch.applicants import AllApplicants
from mentormatch.main.api import main
import pytest
import toml
from mentormatch.main import exceptions
import mentormatch


# def test_allapplicants(applications_path):
#     AllApplicants(applications_path)


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


@pytest.mark.parametrize("filename", ['missing_worksheet.xlsx', 'wrong_row.xlsx'])
def test_exceptions(filename, test_files_dir):

    test_file_path = test_files_dir / filename
    with pytest.raises(exceptions.MentormatchError):
        mentormatch.applicants.AllApplicants(test_file_path)
