from abc import ABC, abstractmethod
from mentormatch.ranker.util import BetterPair
from mentormatch.pair.pair import Pair


class Ranker(ABC):

    @abstractmethod
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        raise NotImplementedError
