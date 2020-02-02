from __future__ import annotations
from mentormatch.api.applicant.applicant_abc import Applicant
from mentormatch.api.utils.enums import ApplicantType
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from mentormatch.api.sorter.sorter_abc import Sorter


class Mentor(Applicant):

    applicant_type = ApplicantType.MENTOR

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        super().__init__(
            applicant_dict=applicant_dict,
            sorter=sorter,
        )
        self.max_pair_count = applicant_dict['max_mentee_count']














