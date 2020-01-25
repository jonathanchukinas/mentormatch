from typing import Tuple
from contextlib import contextmanager
from mentormatch.pair.pair_base import Pair
from .util import BetterPair
from .pair_ranker_abstract import PairRanker


class PairRankerContextMgr(PairRanker):

    def __init__(self):
        self._pair_rankers = {}
        self._current_pair_ranker = None

    def register(self, key: Tuple, pair_ranker: PairRanker) -> None:
        self._pair_rankers[key] = pair_ranker

    @contextmanager
    def set_context(self, key) -> None:
        self._current_pair_ranker = self._pair_rankers[key]
        yield
        self._current_pair_ranker = None

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        if self._current_pair_ranker is None:
            raise RuntimeError()  # TODO set message
        else:
            pair_ranker: PairRanker = self._current_pair_ranker
            return pair_ranker.get_better_pair(pair1, pair2)
