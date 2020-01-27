from mentormatch.api.pair.pair_implementation import Pair
from .util import BetterPair
from .sorter_abc import Sorter


class SorterContextMgr(Sorter):

    def __init__(self, initial_sorter: Sorter, match_sorter: Sorter):
        self._initial_sorter = initial_sorter
        self._match_sorter = match_sorter
        self._current_sorter = None

    def set_initializing_sort(self):
        self._current_sorter = self._initial_sorter

    def set_matching_sort(self):
        self._current_sorter = self._match_sorter

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        pair_ranker: Sorter = self._current_sorter
        return pair_ranker.get_better_pair(pair1, pair2)
