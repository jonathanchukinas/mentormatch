from mentormatch.applicant import Mentor, Mentee
from mentormatch.utils.hash import hash_this_string
from mentormatch.utils.enums import PairType, ApplicantType
from mentormatch.ranker.ranker_abc import Sorter


class Pair:

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
        self.years_delta = self.mentor.years_total - self.mentee.years_total
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
            raise ValueError

    def __eq__(self, other):
        return False    # assuming we've checked for pair compatibility

    # def __ne__(self, other):
    #     return True     # assuming we've checked for pair compatibility

    def __gt__(self, other):
        return self is self.pair_ranker.get_better_pair(self, other)

    def __lt__(self, other):
        return not self >= other

    # def __ge__(self, other):
    #     return self > other

    def __repr__(self):
        classname = self.__class__.__name__     # pragma: no cover
        mentor = str(self.mentor)               # pragma: no cover
        mentee = str(self.mentee)               # pragma: no cover
        obj_id = hex(id(self))                  # pragma: no cover
        return f"<{classname} {mentor}, {mentee} @{obj_id}>"  # pragma:no cover

    def __hash__(self):
        # Used for semi-random sorting
        return self._hash
