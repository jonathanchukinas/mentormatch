from __future__ import annotations
from typing import Sequence, TYPE_CHECKING
from .initializer_abc import Initializer
from mentormatch.api.utils.enums import PairType
if TYPE_CHECKING:
    from mentormatch.api.applicant.applicant_implementation_mentee import Mentee
    from mentormatch.api.pair.pair import Pair


class InitializerPreferred(Initializer):

    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        preferred_mentors = self._mentors.get_applicants_by_wwid(mentee.preferred_wwids)
        #     [
        #     self._mentors.get_applicant_by_wwid(wwid)
        #     for wwid in mentee.preferred_wwids
        # ]
        preferred_pairs = self._get_pairs(
            mentors=preferred_mentors,
            mentee=mentee,
            pair_type=PairType.PREFERRED,
        )
        preferred_pairs_compatible = self._get_compatible_pairs(preferred_pairs)
        return preferred_pairs_compatible


class InitializerRandom(Initializer):

    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        random_pairs = self._get_pairs(
            mentors=self._mentors,
            mentee=mentee,
            pair_type=PairType.RANDOM,
        )
        random_pairs_compatible = self._get_compatible_pairs(random_pairs)
        return random_pairs_compatible
