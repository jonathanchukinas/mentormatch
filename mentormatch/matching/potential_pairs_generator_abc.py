from abc import ABC, abstractmethod


class PotentialPairsGenerator(ABC):

    def __init__(self, mentor_dicts):
        self._mentor_dicts = mentor_dicts

    @abstractmethod
    def assign_potential_pairs_to_mentee(self, mentee):
        pass
