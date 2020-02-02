from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.api.pair.pair import Pair


class Compatibility(ABC):

    @abstractmethod
    def is_compatible(self, pair: Pair) -> bool:
        raise NotImplementedError
