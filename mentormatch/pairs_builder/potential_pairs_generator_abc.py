from abc import ABC, abstractmethod
from mentormatch.pairs.pair_base import BasePair
from typing import Type


class PotentialPairsGenerator(ABC):

    def __init__(self, mentor_dicts, pair_constructor: Type[BasePair]):
        self._mentor_dicts = mentor_dicts
        self._pair_constructor = pair_constructor

    @abstractmethod
    def assign_potential_pairs_to_mentee(self, mentee):
        raise NotImplementedError
