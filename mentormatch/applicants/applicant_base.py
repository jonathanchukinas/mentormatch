"""The ApplicantBase object represents a single applicant. It stores very little
data on its own. Calls to its attributes trigger database calls."""

import hashlib
import collections
# from mentormatch.configuration.fieldschema import locations, genders, fieldschemas
from typing import Dict, Set
from functools import lru_cache
from abc import ABC, abstractmethod
from mentormatch.pairs.pair_base import BasePair


_pref_suffix = "yes maybe no".split()
_pref_attr = ['preference_' + val for val in _pref_suffix]


class ApplicantBase(ABC):

    group = None

    def __init__(self, applicant_dict: Dict):
        self._dict = applicant_dict

        # TODO is this still needed?
        # for pref_suffix, pref_attr in zip(_pref_suffix, _pref_attr):
        #     setattr(self, pref_attr, self._preferences(pref_suffix))

    @abstractmethod
    def assign_pair(self, pair: BasePair) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_pair(self) -> BasePair:
        raise NotImplementedError

    # @property
    # def preference_self(self):
    #     raise NotImplementedError
    #     # TODO where is this used???... return [self.location, self.gender]

    @abstractmethod
    @property
    def paired_with(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def is_available(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def is_paired(self):
        raise NotImplementedError

    @property
    def name(self):
        return ' '.join([self.first_name, self.last_name]).strip()

    @lru_cache
    def __hash__(self):
        hashable_string = (str(self.wwid)).encode()
        self.hash = hashlib.sha1(hashable_string).hexdigest()  # Used for semi-random sorting

    def __str__(self):
        return f'{self.wwid} {self.name}'

    def __getattr__(self, attribute_name):
        return self._dict[attribute_name]

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        obj_id = hex(id(self))  # pragma: no cover
        return f"<{classname} {str(self)} @{obj_id}>"  # pragma: no cover

    @lru_cache
    @property
    def location_and_gender(self) -> Set[str]:
        return {
            self.location,
            self.gender,
            # TODO anything else?
        }

    @lru_cache
    @property
    def preference_yes(self) -> Set[str]:
        return set(self._dict['preference_yes'])

    @lru_cache
    @property
    def preference_maybe(self) -> Set[str]:
        return set(self._dict['preference_maybe'])

    @lru_cache
    @property
    def preference_no(self) -> Set[str]:
        return set(self._dict['preference_no'])

    # def keys(self):
    #     yield from (
    #         field.name
    #         for field in fieldschemas[self.group]
    #         if field.name not in locations + genders
    #     )
    #     yield from _pref_attr  # TODO what is this?
    #     yield 'paired_with'  # TODO implement
    #
    # def __getitem__(self, key):
    #     return getattr(self, key, None)
    #
    # def _preferences(self, yes_no_or_maybe):
    #     if yes_no_or_maybe not in _pref_suffix:
    #         raise ValueError(f"yes_no_or_maybe must be one of {_pref_suffix}. You passed {yes_no_or_maybe}.")  # pragma: no cover
    #     prefs = collections.defaultdict(list)
    #     for value in locations + genders:
    #         key = self[value]
    #         prefs[key].append(value)
    #     return prefs[yes_no_or_maybe]
