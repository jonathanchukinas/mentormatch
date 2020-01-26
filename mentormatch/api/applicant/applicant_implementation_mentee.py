from mentormatch.api.applicant import Applicant
from typing import Dict, List, Set
from mentormatch.api.pair.pair_abc import IPair
from mentormatch.api.utils.enums import ApplicantType


class Mentee(Applicant):

    applicant_type = ApplicantType.MENTEE

    def __init__(self, applicant_dict: Dict):
        super().__init__(applicant_dict)
        self.restart_count = None
        self._assigned_pair = None

    @property
    def preferred_functions(self) -> Set[str]:
        return set(self._dict['preferred_functions'])

    @property
    def preferred_wwids(self) -> List[int]:
        return self._dict['preferred_wwids']

    def assign_pair(self, pair: IPair) -> None:
        self._assigned_pair = pair

    def remove_pair(self) -> IPair:
        removed_pair = self._assigned_pair
        self._assigned_pair = None
        return removed_pair

    @property
    def paired_with(self):
        yield self._assigned_pair

    @property
    def is_paired(self):
        return not self.is_available

    @property
    def is_available(self):
        return self._assigned_pair is None

    @property
    def favored(self):
        return self.favor > 0

    @property
    def selected_at_least_one_preferred_mentor(self) -> bool:
        # TODO rename to something better ... 'wanted_pref_mentors'?...
        return len(self.preferred_wwids) > 0
