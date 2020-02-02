from typing import List
from mentormatch.api.pair.pair import Pair
from .sorter_abc import Sorter
from .util import BetterPair, WeightedSorter, pairs_equal, calc_better_pair, PairAndValue, MinMax
from collections import defaultdict


class SorterAggregatorFavor(Sorter):
    # Evaluate each sub-sorter until a best pair is found.
    # The position of the mentee favor evaluation is dynamically determined by
    # the restart count of both mentees.

    def __init__(
        self,
        sorters: List[Sorter],
        sorter_favor: Sorter,
        sorter_favor_min_position: int,
    ):
        self._sorters = sorters
        self._sorter_favor = sorter_favor
        self._min_favored_position = sorter_favor_min_position

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        favor_index = self._calc_favor_position(pair1, pair2)
        sorters = list(self._sorters)
        sorters.insert(favor_index, self._sorter_favor)
        for sorter in sorters:
            better_pair = sorter.get_better_pair(pair1, pair2)
            if isinstance(better_pair, Pair):
                return better_pair
        return pairs_equal  # pragma: no cover

    def _calc_favor_position(self, pair1: Pair, pair2: Pair):
        mentee1 = pair1.mentee  # TODO
        mentee2 = pair2.mentee
        restart_count = max(mentee1.restart_count, mentee2.restart_count)
        max_pair_ranker_index = len(self._sorters) - 1
        pair_ranker_favor_index = max_pair_ranker_index - restart_count
        favor_index = max(pair_ranker_favor_index, self._min_favored_position)
        return favor_index


class SorterAggregatorWeighted(Sorter):
    # Evaluate all sub-sorters and determine better pair according to the
    # weight assigned to each sub-sorter.

    def __init__(self, weighted_sorters: List[WeightedSorter]):
        self._weighted_sorters = weighted_sorters

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        scores = defaultdict(int)
        for weighted_sorter in self._weighted_sorters:
            sorter = weighted_sorter.pair_ranker
            weight = weighted_sorter.weight
            better_pair = sorter.get_better_pair(pair1, pair2)
            if isinstance(better_pair, Pair):
                scores[better_pair] += weight
        return calc_better_pair(
            pair1=PairAndValue(pair1, scores[pair1]),
            pair2=PairAndValue(pair2, scores[pair2]),
            mode=MinMax.MAX,
        )
