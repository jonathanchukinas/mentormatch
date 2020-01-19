import bisect
from abc import ABC, abstractmethod
from collections import deque
from typing import List, Dict
from mentormatch.applicants.collection_applicants import ApplicantCollection
from mentormatch.pairs_builder.potential_pairs_generator_abc import PotentialPairsGenerator


Pairs = List[Dict]


class BaseMatcher(ABC):

    def __init__(self,
                 mentors: ApplicantCollection,
                 mentees: ApplicantCollection,
                 wwidpairs: Pairs,
                 pairs_builder: PotentialPairsGenerator,
                 ):
        self._mentors = mentors
        self._mentees = mentees
        self._wwidpairs = wwidpairs if wwidpairs is not None else []
        self._pairs_builder = pairs_builder

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def get_wwidpairs(self) -> Pairs:
        return self._wwidpairs


def _perform_matching(mentees_available: List, pairs_getter):

    ################
    # Mentee Deque #
    ################
    mentees_available = deque(sorted(mentees_available, key=lambda m: m.hash))
    for mentee in mentees_available:
        mentee.potential_pairs = pairs_getter(mentee)
        mentee.restart_count = 0

    while len(mentees_available) > 0:

        ###########################
        # Get next potential pair #
        ###########################
        mentee = mentees_available.pop()
        if len(mentee.potential_pairs) > 0:
            # Let's now try to pair this mentee
            pair = mentee.potential_pairs.pop()
        elif mentee.favored and mentee.restart_count < 7:
            # We really want this mentee paired, so we let her go again.
            # She now has a higher liklihood of getting paired.
            mentee.potential_pairs = pairs_getter(mentee)
            mentee.restart_count += 1
            mentees_available.appendleft(mentee)
            continue
        else:
            # This mentee falls out of the matching; remains unpaired.
            continue
        mentor = pair.mentor

        ##############################
        # Assign this potential pair #
        ##############################
        mentee.assigned_pair = pair
        bisect.insort(mentor.assigned_pairs, pair)

        #############################
        # Resolve overloaded mentor #
        #############################
        if mentor.over_capacity:
            rejected_pair = mentor.assigned_pairs.pop(0)
            rejected_mentee = rejected_pair.mentee
            rejected_mentee.assigned_pair = None
            mentees_available.appendleft(rejected_mentee)