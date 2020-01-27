from abc import ABC, abstractmethod
from mentormatch.api.pair.pair_implementation import Pair


class CompatibilityChecker(ABC):  # TODO rename to Compatibility

    @abstractmethod
    def is_compatible(self, pair: Pair) -> bool:  # pragma: no cover
        raise NotImplementedError
