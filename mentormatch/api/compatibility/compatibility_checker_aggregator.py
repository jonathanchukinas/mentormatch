from __future__ import annotations
from typing import TYPE_CHECKING, List
from mentormatch.api.compatibility import Compatibility
if TYPE_CHECKING:
    from mentormatch.api.pair.pair import Pair


class CompatibilityAggregator(Compatibility):
    # Returns True if all registered PairCheckers also return True.

    def __init__(self):
        self._pair_checkers: List[Compatibility] = []

    # def register_pair_checker(self, pair_checker: Compatibility) -> None:
    #     self._pair_checkers.append(pair_checker)

    def register_pair_checkers(self, pair_checkers: List[Compatibility]) -> None:
        self._pair_checkers += pair_checkers

    def is_compatible(self, pair: Pair) -> bool:
        for pair_checker in self._pair_checkers:
            if not pair_checker.is_compatible(pair):
                return False
        return True
