from abc import ABC, abstractmethod
from typing import Sequence
from mentormatch.pair.pair import Pair
from mentormatch.applicant import ApplicantCollection
from mentormatch.ranker import Sorter
from mentormatch.applicant import Mentee


class Initializer(ABC):

    def __init__(self, mentors: ApplicantCollection, sorter: Sorter):
        self._mentors = mentors
        self._sorter = sorter

    @abstractmethod
    def get_potential_pairs(self, mentee: Mentee) -> Sequence[Pair]:
        raise NotImplementedError
