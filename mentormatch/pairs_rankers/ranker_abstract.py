from abc import ABC, abstractmethod
from collections import namedtuple
from unittest.mock import sentinel
from mentormatch.pairs.pair_base import BasePair
from typing import Union, NewType

PairsEqual = sentinel.PairsEqual
BetterPair = Union[PairsEqual, BasePair]


class IPairRanker(ABC):

    @abstractmethod
    def get_better_pair(self, pair1: BasePair, pair2: BasePair) -> BetterPair:
        raise NotImplementedError


YesNoMaybe = NewType('YesNoMaybe', str)  # 'yes', 'no', or 'maybe'
ApplicantType = NewType('ApplicantType', str)  # 'mentor' or 'mentee'
PairAndValue = namedtuple('PairAndValue', 'pair value')


def _calc_better_pair(pair1: PairAndValue, pair2: PairAndValue, mode='max'):
    if pair1.value == pair2.value:
        return PairsEqual
    pairs = sorted([pair1, pair2], key=lambda _pair: _pair.value)
    if mode == 'max':
        return pairs[1].pair
    elif mode == 'min':
        return pairs[0].pair
    else:
        raise ValueError(f"argument 'mode' must be in {['max', 'min']}")