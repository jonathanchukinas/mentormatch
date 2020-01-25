from typing import List
from mentormatch.pair import Pair
from mentormatch.applicant import Mentee
from .pair_ranker_abstract import PairRanker
from .util import BetterPair, WeightedPairRanker, PairsEqual
from collections import defaultdict


class PairRankerMultiWithFavor(PairRanker):

    def __init__(
        self,
        pair_rankers: List[PairRanker],
        pair_ranker_favor: PairRanker,
        pair_ranker_favor_min_position: int,
    ):
        self._pair_rankers: pair_rankers
        self._pair_ranker_favor = pair_ranker_favor
        self._min_favored_position = pair_ranker_favor_min_position

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        favor_index = self._calc_favor_position(pair1, pair2)
        pair_rankers = list(self._pair_rankers)
        pair_rankers.insert(favor_index, self._pair_ranker_favor)
        for pair_ranker in self._pair_rankers:
            better_pair = pair_ranker(pair1, pair2)
            if isinstance(better_pair, Pair):
                return better_pair
        return better_pair

    def _calc_favor_position(self, pair1: Pair, pair2: Pair):
        mentee1: Mentee = pair1.mentee
        mentee2: Mentee = pair2.mentee
        restart_count = max(mentee1.restart_count, mentee2.restart_count)
        max_pair_ranker_index = len(self._pair_rankers) - 1
        pair_ranker_favor_index = max_pair_ranker_index - restart_count
        return max(pair_ranker_favor_index, self._min_favored_position)


class PairRankerMultiWeighted(PairRanker):

    def __init__(self, weighted_pair_rankers: List[WeightedPairRanker]):
        self._weighted_pair_rankers: weighted_pair_rankers

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        # TODO implement hash on pairs
        scores = defaultdict(int)
        for pair_ranker, weight in self._weighted_pair_rankers:
            better_pair = pair_ranker(pair1, pair2)
            if isinstance(better_pair, Pair):
                scores[better_pair] += weight
        if scores[pair1] > scores[pair2]:
            return pair1
        elif scores[pair1] < scores[pair2]:
            return pair2
        else:
            return PairsEqual
