from .applicant_abc import Applicant


# Used as a placeholder. Any pair containing such an object resolves as incompatible


class ApplicantNotFound(Applicant):

    def __init__(self):
        pass
