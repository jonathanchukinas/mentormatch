from abc import ABC


class IMatcher(ABC):

    def __init__(self, mentors, mentees, wwidpairs):
        self._mentors = mentors
        self._mentees = mentees
        self.wwidpairs = wwidpairs if wwidpairs is not None else []

    def generate_pairs(self):
        pass
