from mentormatch.pairs_initializer.pairs_initializer import PairsInitializer
from typing import List
from mentormatch.pairs.pair_base import BasePair


class RandomPairsInitializer(PairsInitializer):

    def get_potential_pairs(self, mentee) -> List[BasePair]:
        pairs = [
            self._pair_constructor(mentor, mentee)
            for mentor in self._mentor_dicts
        ]
        compatible_pairs = list(sorted(filter(lambda p: p.compatible, pairs)))
        return compatible_pairs
