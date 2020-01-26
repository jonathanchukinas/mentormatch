from abc import ABC, abstractmethod
from mentormatch.api.sorter.util import BetterPair
from mentormatch.api.pair.pair_abc import IPair


class Sorter(ABC):

    @abstractmethod
    def get_better_pair(self, pair1: IPair, pair2: IPair) -> BetterPair:
        raise NotImplementedError
