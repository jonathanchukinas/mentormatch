from typing import List
from mentormatch.pairs_initializer.pairs_initializer_abc import PairsInitializer
from mentormatch.pair.pair import Pair


class PairsInitializerPreferred(PairsInitializer):

    def get_potential_pairs(self, mentee) -> List[Pair]:
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


class PairsInitializerRandom(PairsInitializer):

    def get_potential_pairs(self, mentee) -> List[Pair]:
        pairs = [
            self._pair_constructor(mentor, mentee)
            for mentor in self._mentor_dicts
        ]
        compatible_pairs = list(sorted(filter(lambda p: p.compatible, pairs)))
        return compatible_pairs