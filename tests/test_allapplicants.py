from mentormatch.applicants import AllApplicants


def test_allapplicants(applications_path):
    applicants = AllApplicants(applications_path)
    