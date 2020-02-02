from mentormatch.api import compatibility_checker as pc
from mentormatch.api.utils.enums import PairType


class CompatibilityCheckerFactory:

    def __init__(self):
        self._compatibility_checkers = {}

    def register(
        self,
        pair_type: PairType,
        compatibility_checker: pc.Compatibility
    ) -> None:
        self._compatibility_checkers[pair_type] = compatibility_checker

    def get_compatibility_checker(
        self,
        pair_type: PairType
    ) -> pc.Compatibility:
        return self._compatibility_checkers[pair_type]
