from contextlib import contextmanager
from mentormatch.schema.fieldschema import locations, genders
from typing import List
from unittest.mock import sentinel
from collections import Counter

current_mentor = None
mentees = []


PairsEqual = sentinel.PairsEqual


class Pair:

    def __init__(self, mentor, mentee, preferred_match=False):
        self.mentor = mentor
        self.mentee = mentee
        self.preferred_match = preferred_match

    def match_count(self, chooser_type: str, pref_suffix):

        chooser_attr = 'preference_' + pref_suffix  # e.g. 'preference_yes'

        chooser_obj = getattr(self, chooser_type)
        chooser_pref = set(
            chooser_obj[chooser_attr])  # chooser's preferences e.g. (horsham, female, male, west_chester)

        target_type = other_type(chooser_type)
        target_obj = getattr(self, target_type)
        target_char = set(target_obj.preference_self)  # target's characteristics e.g. (horsham, female)

        count_overlap = len(chooser_pref & target_char)  # count of target characteristics desired by chooser
        return count_overlap

    @property
    def compatible(self) -> bool:
        return all((
            self.mentor != self.mentee,
            not self.match_count('mentor', 'no'),
            True if self.preferred_match else not self.match_count('mentee', 'no'),
            self.level_delta >= 0,
            self.years_delta >= 0,
        ))

    @property
    def level_delta(self) -> int:
        mentor_level = self.mentor.position_level
        mentee_level = self.mentee.position_level
        return mentor_level - mentee_level

    @property
    def years_delta(self) -> bool:
        return self.mentor.years_total - self.mentee.years_total

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
        return not self.__eq__(other)

    def __gt__(self, other):
        if self == other:
            return False
        return PairComparison(self, other).gt()

    def __lt__(self, other):
        if self == other:
            return False
        return PairComparison(other, self).gt()

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other


class PairComparison:

    def __init__(self, self_pair: Pair, other_pair: Pair):
        self.self_pair = self_pair
        self.other_pair = other_pair
        self.pairs = [self_pair, other_pair]

    def gt(self) -> bool:

        if not self.self_pair.compatible:
            return False
        elif not self.other_pair.compatible:
            return True

        # else...

        compare_funcs = [
            self.location_and_gender,
            self.level_delta,
            self.years_delta,
            self.rank_order,
            self.wwid_count,
            # 'Early Bird' not implemented
            self.hashorder,
        ]

        ###################
        # Favored Mentees #
        ###################
        max_restart_count = max(pair.mentee.restart_count for pair in self.pairs)
        insert_index = -(1 + max_restart_count)  # always occurs before hashorder, an unfair arbitrary metric
        insert_index = max(len(compare_funcs), insert_index)  # make sure it's never out of range
        compare_funcs.insert(insert_index, favored)

        for func in compare_funcs:
            better_mentee = func()
            if better_mentee is not None:
                return better_mentee

    def _better_pair(self, _list, min_mode=False):
        if _list[0] == _list[1]:
            return PairsEqual
        minmax_func = min if min_mode else max
        best_index = _list.index(minmax_func(_list))
        return self.pairs[best_index]

    def location_and_gender(self, mentor_only=False):
        # Assumption: both mentees have already passed the compatible test
        # The mentee who has more "yeses" wins.
        # If tied, then the mentee with more "maybes" wins.

        applicant_type = 'mentor mentee'.split()
        chooser_types = list(applicant_type)
        if mentor_only:
            chooser_types.remove('mentee')

        for chooser_type in chooser_types:  # i.e. 'mentor' or 'mentee'
            for pref_suffix in "yes maybe".split():
                scores = [
                    pair.match_count(chooser_type, pref_suffix)
                    for pair in self.pairs
                ]
                better_pair = self._better_pair(scores)
                if better_pair is not PairsEqual:
                    return better_pair
        return PairsEqual

    def level_delta(self):
        # The mentee closer to the mentor's level wins
        # The smaller level delta wins
        deltas = [
            pair.level_delta
            for pair in self.pairs
        ]
        return self._better_pair(deltas, min_mode=True)

    def years_delta(self):
        # The mentee closer to the mentor's level wins
        deltas = [
            pair.years_delta
            for pair in self.pairs
        ]
        return self._better_pair(deltas, min_mode=True)

    def rank_order(self):
        # Whichever mentee ranked this mentor higher wins.
        rank_orders = [
            pair.preferredmentor_rankorder
            for pair in self.pairs
        ]
        return self._better_pair(rank_orders, min_mode=True)

    def wwid_count(self):
        # The mentee with more preferred wwids wins.
        wwid_counts = [
            len(pair.mentee.preferred_wwids)
            for pair in self.pairs
        ]
        return self._better_pair(wwid_counts)

    def hashorder(self):
        mentee_hashes = [
            pair.mentee.hash
            for pair in self.pairs
        ]
        return self._better_pair(mentee_hashes)

    def favored(self):
        # The mentee who is more favored (b/c e.g. has been more often or more recently rejected) wins.
        # **This will move up in importance as the mentee fails to pair with one of her preferred mentors.**
        favor = [
            pair.mentee.favor
            for pair in self.pairs
        ]
        return self._better_pair(favor)


def other_type(self_type):
    applicant_types = 'mentor mentee'.split()
    applicant_types.remove(self_type)
    return applicant_types[0]


if __name__ == '__main__':
    pass
