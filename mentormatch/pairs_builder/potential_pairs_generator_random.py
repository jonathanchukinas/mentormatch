from mentormatch.pairs_builder.potential_pairs_generator_abc import PotentialPairsGenerator
from typing import List


class PotentialRandomPairsGenerator(PotentialPairsGenerator):

    def get_pairs(self, mentee) -> List[Pair]:
        pairs = [Pair(mentor, mentee, 'random') for mentor in self.mentors]
        compatible_pairs = sorted(filter(lambda p: p.compatible, pairs))
        return compatible_pairs