from __future__ import annotations
from mentormatch.api.sorter.sorter_abc import Sorter
import bisect
from typing import Dict
from mentormatch.api.applicant import Applicant
from mentormatch.api.pair.pair_abc import IPair
from mentormatch.api.utils.enums import ApplicantType


class Mentor(Applicant):

    applicant_type = ApplicantType.MENTOR

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        super().__init__(
            applicant_dict=applicant_dict,
            sorter=sorter,
        )
        self.max_mentee_count = applicant_dict['max_mentee_count']
        self._assigned_pairs = []

    def assign_pair(self, pair: IPair) -> None:
        bisect.insort(self._assigned_pairs, pair)

    def remove_pair(self) -> IPair:
        # Remove worst-fit pair
        removed_pair = self._assigned_pairs.pop(0)
        return removed_pair

    @property
    def yield_pairs(self):
        yield from self._assigned_pairs

    @property
    def is_available(self):
        return self.mentee_count < self.max_mentee_count

    @property
    def is_paired(self) -> bool:
        return self.mentee_count > 0

    @property
    def over_capacity(self):
        return self.mentee_count > self.max_mentee_count

    @property
    def mentee_count(self):
        return len(self._assigned_pairs)
