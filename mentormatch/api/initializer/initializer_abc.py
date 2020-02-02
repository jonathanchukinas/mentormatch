from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence
from mentormatch.api.pair.pair import Pair
from mentormatch.api.applicant.applicant_collection import ApplicantCollection
from mentormatch.api.sorter.sorter_abc import Sorter
from mentormatch.api.applicant.applicant_implementation_mentor import Mentor
from mentormatch.api.applicant.applicant_implementation_mentee import Mentee
from mentormatch.api.compatibility_checker import Compatibility
from mentormatch.api.utils.enums import PairType


class Initializer(ABC):

    def __init__(
            self,
            mentors: ApplicantCollection,
            compatibility_checker: Compatibility,
            sorter: Sorter
    ):
        self._mentors = mentors
        self._compatibility_checker = compatibility_checker
        self._sorter = sorter

    @abstractmethod
    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        raise NotImplementedError

    def _get_compatible_pairs(self, pairs: Sequence[Pair]):
        is_compatible = self._compatibility_checker.is_compatible
        compatible_pairs = list(filter(
            lambda _pair: is_compatible(_pair),
            pairs,
        ))
        return compatible_pairs

    def _get_pairs(
        self,
        mentors: Sequence[Mentor],
        mentee: Mentee, pair_type: PairType
    ) -> Sequence[Pair]:
        return [
            Pair(
                mentor=mentor,
                mentee=mentee,
                pair_type=pair_type,
                pair_ranker=self._sorter,
            )
            for mentor in mentors
        ]
