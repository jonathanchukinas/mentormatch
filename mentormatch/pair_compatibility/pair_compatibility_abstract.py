from abc import ABC, abstractmethod
from mentormatch.pair.pair_base import Pair


class PairChecker(ABC):

    @abstractmethod
    def is_compatible(self, pair: Pair) -> bool:
        raise NotImplementedError
