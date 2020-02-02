from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.api.sorter.sorter_abc import Sorter
    from .applicant_abc import Applicant


class ApplicantFactory:

    def __init__(self, applicant_class, sorter: Sorter):
        self._applicant_class = applicant_class
        self._sorter = sorter

    def build_applicant(self, applicant_dict: dict) -> Applicant:
        applicant = self._applicant_class(
            applicant_dict=applicant_dict,
            sorter=self._sorter,
        )
        return applicant
