from mentormatch.api.sorter.sorter_abc import Sorter
from .applicant_abc import Applicant


class ApplicantFactory:

    def __init__(self, ranker: Sorter):
        self._ranker = ranker

    def build_applicant(self, applicant_dict: dict) -> Applicant:
        return Applicant(
            applicant_dict=applicant_dict,
            ranker=self._ranker,
        )
