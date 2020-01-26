from mentormatch.api.sorter.sorter_abc import Sorter
from .applicant_abc import Applicant


class ApplicantFactory:

    def __init__(self, applicant_class, ranker: Sorter):
        self._applicant_class = applicant_class
        self._ranker = ranker

    def build_applicant(self, applicant_dict: dict) -> Applicant:
        applicant = self._applicant_class(
            applicant_dict=applicant_dict,
            ranker=self._ranker,
        )
        return applicant
