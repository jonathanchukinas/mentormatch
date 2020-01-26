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
        raise ValueError(f"argument 'mode' must be of type {MinMax}")


def calc_better_pair_list(
    pair1: PairAndValue,
    pair2: PairAndValue,
    descending_list: List
):

    def get_index(pair: PairAndValue):
        try:
            return descending_list.index(pair.value)
        except ValueError:
            raise ValueError(f"{pair.value} not in {descending_list}")

    return calc_better_pair(
        PairAndValue(pair1, get_index(pair1)),
        PairAndValue(pair2, get_index(pair2)),
        mode=MinMax.MIN,
    )


# TODO this needs converted to....
def match_count(self, chooser_type: str, pref_suffix):  # TODO implement enum
    chooser_attr = 'preference_' + pref_suffix  # e.g. 'preference_yes'

    chooser_obj = getattr(self, chooser_type)
    chooser_pref = set(
        chooser_obj[chooser_attr])  # chooser's preferences e.g. (horsham, female, male, west_chester)

    target_type = other_type(chooser_type)
    target_obj = getattr(self, target_type)
    target_char = set(target_obj.preference_self)  # target's characteristics e.g. (horsham, female)

    overlapping_items = chooser_pref & target_char
    count_overlap = len(overlapping_items)  # count of target characteristics desired by chooser
    return count_overlap
