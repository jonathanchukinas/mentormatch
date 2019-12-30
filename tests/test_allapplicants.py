from mentormatch.applicants import AllApplicants
from mentormatch.main.api import main
import pytest
import toml


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

# @pytest.mark.usefixtures("run_api")
# @pytest.fixture(scope='session')
# def result_pairs(pairs_path):
#     pairs_dict = toml.load(pairs_path)['pairs']
#     pairs_dict = {
#         int(key): value
#         for key, value in pairs_dict.items()
#     }
#     return pairs_dict
#
#
# def test_pairs(result_pairs):
#     pairs = result_pairs
#     assert 432198765 in pairs[234567891]
