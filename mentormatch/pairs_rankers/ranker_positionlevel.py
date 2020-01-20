from mentormatch.pairs.pair_base import BasePair
from mentormatch.pairs_rankers.ranker_abstract import IPairRanker, BetterPair, PairsEqual


class RankerPositionLevel(IPairRanker):
    # The mentee closer to the mentor's level wins
    def get_better_pair(self, pair1: BasePair, pair2: BasePair) -> BetterPair:
        if pair1.position_delta == pair2.pos:
            return PairsEqual
        elif pair1.position_delta > pair2.position_delta:
            return pair1
        else:
            return pair2