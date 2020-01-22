from mentormatch.applicants.applicant_base import ApplicantBase
from typing import Dict
from mentormatch.pair.pair_base import Pair
import bisect


class Mentor(ApplicantBase):

    # group = "mentors"

    def __init__(self, applicant_dict: Dict):
        super().__init__(applicant_dict)
        self._assigned_pairs = []

    def assign_pair(self, pair: Pair) -> None:
        bisect.insort(self._assigned_pairs, pair)

    def remove_pair(self) -> Pair:
        # Remove worst-fit pair
        removed_pair = self._assigned_pairs.pop(0)
        return removed_pair

    @property
    def paired_with(self):
        return [str(pair.mentee) for pair in self.assigned_pairs]

    @property
    def is_available(self):
        return self.mentee_count < self.max_mentee_count

    @property
    def is_paired(self):
        return self.mentee_count > 0

    @property
    def over_capacity(self):
        return self.mentee_count > self.max_mentee_count

    @property
    def mentee_count(self):
        return len(self.assigned_pairs)
