from mentormatch.applicants.applicant_base import ApplicantBase
from typing import Dict, List
from mentormatch.pair.pair_base import Pair


class Mentee(ApplicantBase):

    # group = "mentees"  # TODO is this needed?

    def __init__(self, applicant_dict: Dict):
        super().__init__(applicant_dict)
        # self.preferred_mentors = self.gen_preferred_mentors()
        self.restart_count = None
        self._assigned_pair = None
    
    @property
    def preferred_wwids(self) -> List[int]:
        return self._dict['preferred_wwids']

    def assign_pair(self, pair: Pair) -> None:
        self._assigned_pair = pair

    def remove_pair(self) -> Pair:
        removed_pair = self._assigned_pair
        self._assigned_pair = None
        return removed_pair

    @property
    def paired_with(self):
        if self.paired:
            return str(self._assigned_pair.mentor)
        else:
            return '...unpaired...'

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
