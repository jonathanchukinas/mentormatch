from __future__ import annotations
from mentormatch.api.sorter.sorter_abc import Sorter
from mentormatch.api.applicant import Applicant
from typing import Dict, List, Set
from mentormatch.api.pair.pair_abc import IPair
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
        self._assigned_pairs = []
        self.preferred_functions: Set[str] = set(self._dict['preferred_functions'])
        self.preferred_wwids: List[int] = self._dict['preferred_wwids']

    def assign_pair(self, pair: IPair) -> None:
        self._assigned_pairs.append(pair)

    def remove_pair(self) -> IPair:
        return self._assigned_pairs.pop()

    @property
    def yield_pairs(self):  # TODO return a Pair, but it implies a mentor. Fix terms
        yield from self._assigned_pairs

    @property
    def is_available(self):
        return len(self._assigned_pairs) == 0

    @property
    def is_paired(self) -> bool:
        return not self.is_available

    @property
    def favored(self):
        return self.favor > 0
