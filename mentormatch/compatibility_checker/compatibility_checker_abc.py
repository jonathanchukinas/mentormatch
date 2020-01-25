from abc import ABC, abstractmethod
from mentormatch.pair.pair import Pair


class CompatibilityChecker(ABC):

    @abstractmethod
    def is_compatible(self, pair: Pair) -> bool:
        raise NotImplementedError
