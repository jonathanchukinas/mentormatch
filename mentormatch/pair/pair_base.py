from abc import ABC, abstractmethod
from mentormatch.pair_ranker.pair_comparison import PairComparison
from mentormatch.applicants.applicant_base import ApplicantBase, ApplicantType
from functools import lru_cache
from mentormatch.applicants import Mentor, Mentee


current_mentor = None
mentees = []


class Pair(ABC):

    def __init__(
            self,
            mentor: Mentor,
            mentee: Mentee,
    ):
        self.mentor: Mentor = mentor
        self.mentee: Mentee = mentee

    def match_count(self, chooser_type: str, pref_suffix):
        chooser_attr = 'preference_' + pref_suffix  # e.g. 'preference_yes'

        chooser_obj = getattr(self, chooser_type)
        chooser_pref = set(
            chooser_obj[chooser_attr])  # chooser's preferences e.g. (horsham, female, male, west_chester)

        target_type = other_type(chooser_type)
        target_obj = getattr(self, target_type)
        target_char = set(target_obj.preference_self)  # target's characteristics e.g. (horsham, female)

        overlapping_items = chooser_pref & target_char
        count_overlap = len(overlapping_items)  # count of target characteristics desired by chooser
        return count_overlap

    def get_applicant(self, applicant_type: ApplicantType, return_other=False):
        types = 'mentor mentee'.split()
        if applicant_type not in types:
            raise ValueError
        if return_other:
            applicant_type = types.remove(applicant_type)[0]
        if applicant_type == 'mentor':
            return self.mentor
        else:
            return self.mentee

    @lru_cache()
    @property
    def compatible(self) -> bool:
        raise NotImplementedError

    @property
    def level_delta(self) -> int:
        mentor_level = self.mentor.position_level
        mentee_level = self.mentee.position_level
        return mentor_level - mentee_level

    @property
    def years_delta(self) -> bool:
        return self.mentor.years_total - self.mentee.years_total

    @abstractmethod
    @property
    def preferred(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def random(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.mentee == other.mentee and self.mentor == other.mentor

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        better_pair = PairComparison(self, other).get_better_pair()
        return self != other and self is better_pair

    def __lt__(self, other):
        return not self >= other

    def __ge__(self, other):
        return self == other or self > other

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        mentor_repr = str(self.mentor)  # pragma: no cover
        mentee_repr = str(self.mentee)  # pragma: no cover
        obj_id = hex(id(self))  # pragma: no cover
        return f"<{classname} {mentor_repr}, {mentee_repr} @{obj_id}>"  # pragma: no cover


def other_type(self_type):
    applicant_types = 'mentor mentee'.split()
    applicant_types.remove(self_type)
    return applicant_types[0]


if __name__ == '__main__':
    pass

