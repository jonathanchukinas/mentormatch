from collections import deque
from mentormatch.api.applicant.applicant_collection import ApplicantCollection
from mentormatch.api.initializer import Initializer
from mentormatch.api.sorter.sorter_context_mgr import SorterContextMgr


class Matcher:

    def __init__(
            self,
            mentors: ApplicantCollection,
            mentees: ApplicantCollection,
            initializer: Initializer,
            ranker_context_mgr: SorterContextMgr,
    ):
        self._mentors = mentors
        self._mentees = mentees
        self._initializer = initializer
        self._sorter_context_mgr = ranker_context_mgr

    def execute(self) -> None:

        ################
        # Mentee Deque #
        ################
        unpaired_mentees = deque(filter(lambda _mentee: _mentee.is_available, self._mentees))
        self._sorter_context_mgr.set_initializing_sort()
        for mentee in unpaired_mentees:
            mentee.potential_pairs = self._initializer.get_potential_pairs(mentee)
            # TODO sort pairs here
            mentee.restart_count = 0

        self._sorter_context_mgr.set_matching_sort()
        while len(unpaired_mentees) > 0:

            ###########################
            # Get next potential pair #
            ###########################
            mentee = unpaired_mentees.pop()
            if len(mentee.potential_pairs) > 0:
                # Let's now try to pair this mentee
                pair = mentee.potential_pairs.pop()
                mentor = pair.mentor
            elif mentee.favored and mentee.restart_count < 7:
                # We really want this mentee paired, so we let her go again.
                # She is more likely to get paired next time around.
                mentee.potential_pairs = self._initializer.get_potential_pairs(mentee)
                mentee.restart_count += 1
                unpaired_mentees.appendleft(mentee)
                continue
            else:
                # This mentee falls out of the matching; remains unpaired.
                continue

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
