from typing import Sequence
from mentormatch.pair.pair import Pair
from .initializer_abc import Initializer
from mentormatch.utils.enums import PairType
from mentormatch.applicant import Mentee


class InitializerPreferred(Initializer):

    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        preferred_mentors = [
            self._mentors.get_applicant_by_wwid(wwid)
            for wwid in mentee.preferred_wwids
        ]
        preferred_pairs = [
            Pair(
                mentor=mentor,
                mentee=mentee,
                pair_type=PairType.PREFERRED,
                pair_ranker=self._sorter,
            )
            for mentor in preferred_mentors
        ]
        preferred_pairs_compatible = list(filter(lambda _pair: _pair.compatible, preferred_pairs))
        return preferred_pairs_compatible


class InitializerRandom(Initializer):

    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        random_pairs = [
            Pair(
                mentor=mentor,
                mentee=mentee,
                pair_type=PairType.RANDOM,
                pair_ranker=self._sorter,
            )
            for mentor in self._mentors
        ]
        random_pairs_compatible = list(filter(lambda _pair: _pair.compatible, random_pairs))
        return random_pairs_compatible


