"""The Applicant object represents a single applicant. It stores very
little data on its own. Calls to its attributes trigger database calls."""
from __future__ import annotations
import bisect
from abc import ABC
from mentormatch.utils import hash_this_string
from mentormatch.utils import YesNoMaybe
from typing import Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.api.sorter.sorter_abc import Sorter
    from mentormatch.api.pair.pair import Pair


class Applicant(ABC):

    applicant_type = None

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        _d = applicant_dict
        self._dict = _d
        self._sorter = sorter
        self.skills: Set[str] = set(_d['skills'])
        self.function = _d['function']
        self.wwid = _d['wwid']
        self.name = f"{_d['last_name']}, {_d['first_name']}".title()
        self.position_level = _d['position_level']
        self.years = _d['years_total']
        self.location_and_gender = {_d['location'], _d['gender']}
        self._yesnomaybe = {
            YesNoMaybe.YES: set(_d['preference_yes']),
            YesNoMaybe.NO: set(_d['preference_no']),
            YesNoMaybe.MAYBE: set(_d['preference_maybe']),
        }
        self.max_pair_count = None
        self._assigned_pairs = []

    @property
    def application_dict(self) -> Dict:
        return self._dict

    def assign_pair(self, pair: Pair) -> None:
        bisect.insort(self._assigned_pairs, pair)

    @property
    def yield_pairs(self):
        yield from self._assigned_pairs

    @property
    def is_available(self):
        return self.pair_count < self.max_pair_count

    @property
    def is_paired(self) -> bool:
        return self.pair_count > 0

    @property
    def pair_count(self):
        return len(self._assigned_pairs)

    @property
    def over_capacity(self):
        return self.pair_count > self.max_pair_count

    def remove_pair(self) -> Pair:
        # Remove worst-fit pair
        removed_pair = self._assigned_pairs.pop(0)
        return removed_pair

    #################################################
    # Properties based on imported application data #
    #################################################

    def get_preference(
        self,
        yesnomaybe: YesNoMaybe
    ) -> Set[str]:
        return self._yesnomaybe[yesnomaybe]

    def __hash__(self):
        return hash_this_string(self.wwid)

    def __str__(self):
        # name_with_underscores = self.name.lower().replace(' ', '_')
        return f'{self.name} {self.wwid}'

    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__
        obj_id = hex(id(self))
        return f"<{classname} {str(self)} @{obj_id}>"
