from mentormatch.applicants.applicant_base import ApplicantType, ApplicantBase
from mentormatch.pair.pair_base import Pair
from mentormatch.pair_ranker.pair_ranker_abstract import PairRanker
from mentormatch.pair_ranker.util import BetterPair
from typing import List


class PairRankerBuilder(PairRanker):
    # Returns True if all registered PairRankers also return True.

    def __init__(self):
        self._pair_rankers: List[PairRanker] = []

    def register_pair_checker(self, pair_checker: PairRanker) -> None:
        self._pair_rankers.append(pair_checker)

    def register_pair_checkers(self, pair_checkers: List[PairRanker]) -> None:
        self._pair_rankers += pair_checkers

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        for pair_rankers in self._pair_rankers:
            if not pair_rankers.get_better_pair(pair1, pair2):
                return False
        return True
