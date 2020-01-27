from collections import namedtuple
from typing import Union, List, Type
from unittest.mock import sentinel
from mentormatch.api.pair.pair_abc import IPair
from mentormatch.api.utils.enums import MinMax


class PairsEqual:
    pass


# PairsEqual = sentinel.PairsEqual
pairs_equal = PairsEqual()
BetterPair = Union[PairsEqual, IPair]
PairAndValue = namedtuple('PairAndValue', 'pair value')
WeightedPairRanker = namedtuple('WeightedPairRanker', 'pair_ranker weight')


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


# def calc_better_pair_list(
#     pair1: PairAndValue,
#     pair2: PairAndValue,
#     descending_list: List
# ):
#
#     def get_index(pair: PairAndValue):
#         try:
#             return descending_list.index(pair.value)
#         except ValueError:
#             raise ValueError(f"{pair.value} not in {descending_list}")
#
#     return calc_better_pair(
#         PairAndValue(pair1, get_index(pair1)),
#         PairAndValue(pair2, get_index(pair2)),
#         mode=MinMax.MIN,
#     )
