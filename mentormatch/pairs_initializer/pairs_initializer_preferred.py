from typing import List
from mentormatch.pairs_initializer.pairs_initializer import PairsInitializer
from mentormatch.pairs.pair_base import BasePair


class PreferredPairsInitializer(PairsInitializer):

    def get_potential_pairs(self, mentee) -> List[BasePair]:
        preferred_mentors = reversed([
            mentee.applicants.mentors.get_applicant_by_wwid(wwid)
            for wwid in mentee.preferred_wwids
        ])
        preferred_pairs = [
            self._pair_constructor(mentor, mentee)
            for mentor in preferred_mentors
        ]
        # Strip out incompatible pairs
        preferred_pairs = list(filter(lambda p: p.compatible, preferred_pairs))
        return preferred_pairs
