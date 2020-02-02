from __future__ import annotations
from mentormatch.api.sorter.sorter_abc import Sorter
from typing import Dict
from mentormatch.api.applicant import Applicant
from mentormatch.api.utils.enums import ApplicantType


class Mentor(Applicant):

    applicant_type = ApplicantType.MENTOR

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        super().__init__(
            applicant_dict=applicant_dict,
            sorter=sorter,
        )
        self.max_pair_count = applicant_dict['max_mentee_count']














