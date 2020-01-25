from typing import List
from mentormatch.compatibility_checker.compatibility_checker_abstract import CompatibilityChecker
from mentormatch.pair.pair_base import Pair


class CompatibilityCheckerAggregator(CompatibilityChecker):
    # Returns True if all registered PairCheckers also return True.

    def __init__(self):
        self._pair_checkers: List[CompatibilityChecker] = []

    def register_pair_checker(self, pair_checker: CompatibilityChecker) -> None:
        self._pair_checkers.append(pair_checker)

    def register_pair_checkers(self, pair_checkers: List[CompatibilityChecker]) -> None:
        self._pair_checkers += pair_checkers

    def is_compatible(self, pair: Pair) -> bool:
        for pair_checker in self._pair_checkers:
            if not pair_checker.is_compatible(pair):
                return False
        return True
