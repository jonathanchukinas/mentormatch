from __future__ import annotations
from abc import ABC, abstractmethod
from mentormatch.api.sorter.util import BetterPair
from mentormatch.api.pair.pair import Pair


class Sorter(ABC):

    @abstractmethod
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        raise NotImplementedError
