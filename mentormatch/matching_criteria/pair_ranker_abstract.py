from abc import ABC, abstractmethod
from unittest.mock import sentinel
from mentormatch.pairs.pair_base import BasePair
from typing import Union


PairsEqual = sentinel.PairsEqual
BetterPair = Union[PairsEqual, BasePair]


class IPairRanker(ABC):

    @abstractmethod
    def get_better_pair(self, pair1: BasePair, pair2: BasePair) -> BetterPair:
        raise NotImplementedError
