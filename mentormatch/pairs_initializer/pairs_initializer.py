from abc import ABC, abstractmethod
from mentormatch.pairs.pair_base import BasePair
from typing import Type, List


class PairsInitializer(ABC):

    def __init__(self, mentor_dicts, pair_constructor: Type[BasePair]):
        self._mentor_dicts = mentor_dicts
        self._pair_constructor = pair_constructor

    @abstractmethod
    def get_potential_pairs(self, mentee) -> List[BasePair]:
        raise NotImplementedError
