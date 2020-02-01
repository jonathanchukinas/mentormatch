"""The Applicant object represents a single applicant. It stores very
little data on its own. Calls to its attributes trigger database calls."""
from __future__ import annotations
from typing import Dict, Set
from mentormatch.api.pair.pair_abc import IPair
from mentormatch.api.utils.enums import YesNoMaybe
from mentormatch.api.utils.hash import hash_this_string
from mentormatch.api.sorter.sorter_abc import Sorter
from abc import ABC, abstractmethod


class Applicant(ABC):

    applicant_type = None  # TODO this should not be a class attribute!!

    def __init__(self, applicant_dict: Dict, sorter: Sorter):
        self._dict = applicant_dict
        self._ranker = sorter
        self.skills: Set[str] = set(applicant_dict['skills'])
        self.functions: Set[str] = set(applicant_dict['function'])
        self.wwid = applicant_dict['wwid']
        self._hash = hash_this_string(self.wwid)
        self.name = f"{applicant_dict['last_name']}, {applicant_dict['first_name']}".title()
        self.position_level = self._dict['position_level']
        self.years = self._dict['years_total']
        self.location_and_gender = {
            self._dict['location'], self._dict['gender']}
        self._yesnomaybe = {
            YesNoMaybe.YES: set(self._dict['preference_yes']),
            YesNoMaybe.NO: set(self._dict['preference_no']),
            YesNoMaybe.MAYBE: set(self._dict['preference_maybe']),
        }

    @property
    def application_dict(self) -> Dict:
        return self._dict

    @abstractmethod
    def assign_pair(self, pair: IPair) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def remove_pair(self) -> IPair:  # pragma: no cover
        raise NotImplementedError

    @property
    @abstractmethod
    def yield_pairs(self):  # pragma: no cover
        raise NotImplementedError

    @property
    @abstractmethod
    def is_available(self) -> bool:  # pragma: no cover
        raise NotImplementedError

    @property
    @abstractmethod
    def is_paired(self) -> bool:  # pragma: no cover
        raise NotImplementedError

    #################################################
    # Properties based on imported application data #
    #################################################

    def get_preference(
        self,
        yesnomaybe: YesNoMaybe
    ) -> Set[str]:
        return self._yesnomaybe[yesnomaybe]

    def __hash__(self):
        return self._hash

    def __str__(self):
        # name_with_underscores = self.name.lower().replace(' ', '_')
        return f'{self.name} {self.wwid}'

    def __repr__(self):
        classname = self.__class__.__name__
        obj_id = hex(id(self))
        return f"<{classname} {str(self)} @{obj_id}>"
