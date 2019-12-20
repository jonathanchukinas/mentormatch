from mentormatch.applicants import AllApplicants
from mentormatch.main.api import main


def test_allapplicants(applications_path):
    applicants = AllApplicants(applications_path)


def test_api(applications_path):
    main(applications_path)
