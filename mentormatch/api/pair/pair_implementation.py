from __future__ import annotations
from mentormatch.api.utils.hash import hash_this_string
from mentormatch.api.utils.enums import PairType, ApplicantType
from .pair_abc import IPair
from mentormatch.api.applicant import Mentor, Mentee
from mentormatch.api.sorter.sorter_abc import Sorter


class Pair(IPair):

    def __init__(
            self,
            mentor: Mentor,
            mentee: Mentee,
            pair_type: PairType,
            pair_ranker: Sorter,
    ):
        self.mentor: Mentor = mentor
        self.mentee: Mentee = mentee
        self._applicants = [mentor, mentee]
        self.pair_type = pair_type
        self.pair_ranker = pair_ranker
        self._hash = hash_this_string(
            str(self.mentor.wwid) + str(self.mentee.wwid))
        self.years_delta = self.mentor.years - self.mentee.years
        self.level_delta = self.mentor.position_level - \
            self.mentee.position_level

    def get_applicant(self, applicant_type: ApplicantType, return_other=False):
        if return_other:
            applicant_type = applicant_type.get_other()
        if applicant_type is ApplicantType.MENTOR:
            return self.mentor
        elif applicant_type is ApplicantType.MENTEE:
            return self.mentee
        else:
            raise ValueError  # pragma: no cover

    # def __eq__(self, other):
    #     return False    # assuming we've checked for pair compatibility

    # def __ne__(self, other):
    #     return True     # assuming we've checked for pair compatibility

    def __gt__(self, other):
        return self is self.pair_ranker.get_better_pair(self, other)

    def __lt__(self, other):
        return not self >= other

    def __ge__(self, other):
        return self > other

    def __repr__(self):  # pragma: no cover
        classname = self.__class__.__name__     
        mentor = str(self.mentor)
        mentee = str(self.mentee)
        obj_id = hex(id(self))
        return f"<{classname} {mentor}, {mentee} @{obj_id}>"

    def __hash__(self):
        # Used for semi-random sorting
        return self._hash
