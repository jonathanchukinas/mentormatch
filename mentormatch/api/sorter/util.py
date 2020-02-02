from __future__ import annotations
from collections import namedtuple
from typing import Union
from mentormatch.api.pair.pair import Pair
from mentormatch.api.utils.enums import MinMax


class PairsEqual:
    pass


# PairsEqual = sentinel.PairsEqual
pairs_equal = PairsEqual()
BetterPair = Union[PairsEqual, Pair]
PairAndValue = namedtuple('PairAndValue', 'pair value')
WeightedSorter = namedtuple('WeightedSorter', 'pair_ranker weight')


# TODO make sure clients implement enum too
def calc_better_pair(pair1: PairAndValue, pair2: PairAndValue, mode: MinMax) -> BetterPair:
    if pair1.value == pair2.value:
        return pairs_equal
    pairs = sorted([pair1, pair2], key=lambda _pair: _pair.value)
    if mode is MinMax.MAX:
        return pairs[1].pair
    elif mode is MinMax.MIN:
        return pairs[0].pair
    else:
        raise ValueError(f"argument 'mode' must be of type {MinMax}")  # pragma: no cover
