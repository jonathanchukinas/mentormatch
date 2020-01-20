from abc import ABC, abstractmethod
from unittest.mock import sentinel
from mentormatch.pairs.pair_comparison import PairComparison
from mentormatch.applicants.applicant_base import ApplicantBase
from mentormatch.pairs import checks



current_mentor = None
mentees = []


PairsEqual = sentinel.PairsEqual


class BasePair(ABC):

    def __init__(
            self,
            mentor: ApplicantBase,
            mentee: ApplicantBase,
            match_type: str,  # 'preferred' or 'random'  # TODO replace this with subclasses
    ):
        self.mentor: ApplicantBase = mentor
        self.mentee: ApplicantBase = mentee
        self.match_type = match_type  # TODO replace this with subclasses

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

    @property
    def compatible(self) -> bool:
        return all((
            checks.are_different_people(self.mentor, self.mentee),
            checks.mentor_sees_no_dealbreakers(self.mentor, self.mentee),
        ))

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

    @property
    def preferredmentor_rankorder(self) -> int:
        # Whichever mentee ranked this mentor higher wins.
        mentor_wwid = self.mentor.wwid
        mentee_preferredwwids: list = self.mentee.preferred_wwids
        rankorder = mentee_preferredwwids.index(mentor_wwid)
        return rankorder

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

    # def __le__(self, other):
    #     return not self > other

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

