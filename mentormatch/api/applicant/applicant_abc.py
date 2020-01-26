"""The Applicant object represents a single applicant. It stores very
little data on its own. Calls to its attributes trigger database calls."""

from typing import Dict, Set
from functools import lru_cache
# from abc import ABC, abstractmethod
from mentormatch.api.pair.pair_abc import IPair
from mentormatch.api.utils.enums import YesNoMaybe
from mentormatch.api.utils.hash import hash_this_string
from mentormatch.api.sorter.sorter_abc import Sorter


class Applicant:

    applicant_type = None

    def __init__(self, applicant_dict: Dict, ranker: Sorter):
        self._dict = applicant_dict
        self._ranker = ranker
        self.skills: Set[str] = set(self._dict['skills'])
        self.functions: Set[str] = set(self._dict['function'])
        self.wwid = set(self._dict['wwid'])
        self._hash = hash_this_string(self.wwid)
        self.name = ' '.join([self.first_name, self.last_name]).strip()
        self.position_level = self._dict['position_level']
        self.years_experience = self._dict['years_experience']
        self.location_and_gender = {
            self._dict['location'], self._dict['gender']}
        self._yesnomaybe = {
            YesNoMaybe.YES: set(self._dict['preference_yes']),
            YesNoMaybe.NO: set(self._dict['preference_no']),
            YesNoMaybe.MAYBE: set(self._dict['preference_maybe']),
        }

    # @abstractmethod
    def assign_pair(self, pair: IPair) -> None:
        raise NotImplementedError

    # @abstractmethod
    def remove_pair(self) -> IPair:
        raise NotImplementedError

    @property
    # @abstractmethod
    def paired_with(self):
        raise NotImplementedError

    @property
    # @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @property
    # @abstractmethod
    def is_paired(self) -> bool:
        raise NotImplementedError

    #################################################
    # Properties based on imported application data #
    #################################################

    @lru_cache
    def get_preference_location_and_gender(
        self,
        yesnomaybe: YesNoMaybe
    ) -> Set[str]:
        return self._yesnomaybe[yesnomaybe]

    def __hash__(self):
        return self._hash

    def __str__(self):
        return f'{self.wwid} {self.name}'

    def __getattr__(self, attribute_name):
        return self._dict[attribute_name]

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        obj_id = hex(id(self))  # pragma: no cover
        return f"<{classname} {str(self)} @{obj_id}>"  # pragma: no cover
