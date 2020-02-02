from abc import ABC, abstractmethod
from mentormatch.api.pair.pair import Pair


class Compatibility(ABC):

    @abstractmethod
    def is_compatible(self, pair: Pair) -> bool:  # pragma: no cover
        raise NotImplementedError
