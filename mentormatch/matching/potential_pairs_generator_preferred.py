from typing import List

from mentormatch.matching.potential_pairs_generator_abc import PotentialPairsGenerator


class PotentialPreferredPairsGenerator(PotentialPairsGenerator):

    def assign_potential_pairs_to_mentee(self, mentee):
        pairs = self._assign_potential_pairs_to_mentee(mentee)
        # TODO assign this to the mentee now.

    def _assign_potential_pairs_to_mentee(mentee) -> List[Pair]:
        preferred_mentors = reversed([
            mentee.applicants.mentors.wwid_get(wwid)
            for wwid in mentee.preferred_wwids
        ])
        preferred_pairs = [Pair(mentor, mentee, 'preferred') for mentor in preferred_mentors]
        preferred_and_compatible_pairs = list(filter(lambda p: p.compatible, preferred_pairs))
        return preferred_and_compatible_pairs