"""The ApplicantBase object represents a single applicant. It stores very
little data on its own. Calls to its attributes trigger database calls."""

import hashlib
from typing import Dict, Set
from functools import lru_cache
from abc import ABC, abstractmethod
from mentormatch.pair.pair_base import Pair
from mentormatch.utils.enums import YesNoMaybe


class ApplicantBase(ABC):

    applicant_type = None

    def __init__(self, applicant_dict: Dict):
        self._dict = applicant_dict

    @abstractmethod
    def assign_pair(self, pair: Pair) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_pair(self) -> Pair:
        raise NotImplementedError

    @abstractmethod
    @property
    def paired_with(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    @property
    def is_paired(self) -> bool:
        raise NotImplementedError

    #################################################
    # Properties based on imported application data #
    #################################################

    @lru_cache
    @property
    def skills(self) -> Set[str]:
        
        return set(self._dict['skills'])

    @property
    def functions(self) -> Set[str]:
        return set(self._dict['function'])

    @property
    def name(self) -> str:
        return ' '.join([self.first_name, self.last_name]).strip()

    @property
    def wwid(self) -> int:
        return self._dict['wwid']  # TODO need error checking?

    @property
    def position_level(self) -> int:
        return self._dict['position_level']  # TODO need error checking?

    @property
    def years_experience(self) -> float:
        return self._dict['years_experience']  # TODO need error checking?

    @lru_cache
    @property
    def location_and_gender(self) -> Set[str]:
        return {self.location, self.gender}

    # @lru_cache
    # @property
    # def preference_yes(self) -> Set[str]:
    #     return set(self._dict['preference_yes'])

    # @lru_cache
    # @property
    # def preference_maybe(self) -> Set[str]:
    #     return set(self._dict['preference_maybe'])

    # @lru_cache
    # @property
    # def preference_no(self) -> Set[str]:
    #     return set(self._dict['preference_no'])

    @lru_cache
    def get_preference_location_and_gender(
        self,
        yesnomaybe: YesNoMaybe
    ) -> Set[str]:
        if yesnomaybe is YesNoMaybe.YES:
            return set(self._dict['preference_yes'])
        elif yesnomaybe is YesNoMaybe.MAYBE:
            return set(self._dict['preference_maybe'])
        elif yesnomaybe is YesNoMaybe.NO:
            return set(self._dict['preference_no'])
        else:
            raise NotImplementedError

    @lru_cache
    def __hash__(self):
        # Used for semi-random sorting
        hashable_string = (str(self.wwid)).encode()
        self.hash = hashlib.sha1(hashable_string).hexdigest()

    def __str__(self):
        return f'{self.wwid} {self.name}'

    def __getattr__(self, attribute_name):
        return self._dict[attribute_name]

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        obj_id = hex(id(self))  # pragma: no cover
        return f"<{classname} {str(self)} @{obj_id}>"  # pragma: no cover
