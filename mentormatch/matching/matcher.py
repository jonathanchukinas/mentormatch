from collections import deque
from typing import List, Dict
from mentormatch.applicant.applicant_collection import ApplicantCollection
from mentormatch.pairs_initializer.pairs_initializer_abc import PairsInitializer


Pairs = List[Dict]  # TODO needed?


class Matcher:

    def __init__(
            self,
            mentors: ApplicantCollection,
            mentees: ApplicantCollection,
            pairs_initializer: PairsInitializer,
    ):
        self._mentors = mentors
        self._mentees = mentees
        self._pairs_initializer = pairs_initializer

    def _get_unpaired_mentees(self):
        return deque(sorted(
            self._mentees.get_available_applicants(),
            key=lambda mentee: hash(mentee)
        ))

    def run(self) -> None:

        ################
        # Mentee Deque #
        ################
        unpaired_mentees = self._get_unpaired_mentees()
        for mentee in unpaired_mentees:
            mentee.potential_pairs = self._pairs_initializer.get_potential_pairs(mentee)
            mentee.restart_count = 0

        while len(unpaired_mentees) > 0:

            ###########################
            # Get next potential pair #
            ###########################
            mentee = unpaired_mentees.pop()
            if len(mentee.potential_pairs) > 0:
                # Let's now try to pair this mentee
                pair = mentee.potential_pairs.pop()
            elif mentee.favored and mentee.restart_count < 7:
                # We really want this mentee paired, so we let her go again.
                # She is more likely to get paired next time around.
                mentee.potential_pairs = self._pairs_initializer.get_potential_pairs(mentee)
                mentee.restart_count += 1
                unpaired_mentees.appendleft(mentee)
                continue
            else:
                # This mentee falls out of the matching; remains unpaired.
                continue
            mentor = pair.mentor

            ##############################
            # Assign this potential pair #
            ##############################
            mentee.assign_pair(pair)
            mentor.assign_pair(pair)

            #############################
            # Resolve overloaded mentor #
            #############################
            if mentor.over_capacity:
                rejected_pair = mentor.remove_pair()
                rejected_mentee = rejected_pair.mentee
                rejected_mentee.remove_pair()
                unpaired_mentees.appendleft(rejected_mentee)
