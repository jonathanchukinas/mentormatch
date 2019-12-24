# --- Standard Library Imports ------------------------------------------------
from collections import deque
import bisect
from typing import List

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants import Pair
from mentormatch.applicants import AllApplicants, Mentee


class Matching:

    def __init__(self, applicants: AllApplicants):
        self.applicants = applicants

    def preferred_matching(self):

        ###################
        # Collect Mentees #
        ###################
        all_mentees: List[Mentee] = list(self.applicants.mentees)
        mentees_available = [
            mentee
            for mentee in all_mentees
            if mentee.selected_preferred_mentors
        ]
        pairs_getter = potential_preferred_pairs

        _matching(
            mentees_available=mentees_available,
            pairs_getter=pairs_getter,
        )

    def random_matching(self):

        ###################
        # Collect Mentors #
        ###################
        mentors_available = filter(lambda m: m.below_capacity, self.applicants.mentors)
        mentors_available = tuple(sorted(mentors_available, key=lambda m: m.hash))
        pairs_getter = PotentialRandomPairCreator(mentors_available).get_pairs

        ###################
        # Collect Mentees #
        ###################
        mentees_available = list(filter(lambda m: not m.paired, self.applicants.mentees))

        _matching(
            mentees_available=mentees_available,
            pairs_getter=pairs_getter,
        )


def _matching(mentees_available: List, pairs_getter):

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
        elif mentee.favored and mentee.restart_count < 6:
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


def potential_preferred_pairs(mentee) -> List[Pair]:
    preferred_mentors = reversed([
        mentee.applicants.mentors.wwid_get(wwid)
        for wwid in mentee.preferred_wwids
    ])
    return [Pair(mentor, mentee) for mentor in preferred_mentors]


class PotentialRandomPairCreator:

    def __init__(self, mentors):
        self.mentors = mentors

    def get_pairs(self, mentee) -> List[Pair]:
        pairs = [Pair(mentor, mentee) for mentor in self.mentors]
        compatible_pairs = sorted(filter(lambda p: p.compatible, pairs))
        return compatible_pairs
