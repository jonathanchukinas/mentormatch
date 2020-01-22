from abc import ABC, abstractmethod
from mentormatch.pair.pair_base import Pair
from typing import Type, List


class PairsInitializer(ABC):

    def __init__(self, mentor_dicts, pair_constructor: Type[Pair]):
        self._mentor_dicts = mentor_dicts
        self._pair_constructor = pair_constructor

    @abstractmethod
    def get_potential_pairs(self, mentee) -> List[Pair]:
        raise NotImplementedError
