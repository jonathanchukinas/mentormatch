from __future__ import annotations
from mentormatch.api.sorter.sorter_abc import Sorter
from mentormatch.api.applicant import Applicant
from typing import Dict, List, Set
from mentormatch.api.utils.enums import ApplicantType


class Mentee(Applicant):

    applicant_type = ApplicantType.MENTEE

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        super().__init__(
            applicant_dict=applicant_dict,
            sorter=sorter,
        )
        self.favor = applicant_dict['favor']
        self.restart_count = None
        self.preferred_functions: Set[str] = set(self._dict['preferred_functions'])
        self.preferred_wwids: List[int] = self._dict['preferred_wwids']
        self.max_pair_count = 1

    @property
    def favored(self):
        return self.favor > 0
