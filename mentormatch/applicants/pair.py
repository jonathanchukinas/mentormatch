from contextlib import contextmanager
from mentormatch.schema.fieldschema import locations, genders
from typing import List
from unittest.mock import sentinel
from collections import Counter

current_mentor = None
mentees = []


PairsEqual = sentinel.PairsEqual


class Pair:

    def __init__(
            self,
            mentor,
            mentee,
            match_type,  # 'preferred' or 'random'
    ):
        self.mentor = mentor
        self.mentee = mentee
        self.match_type = match_type

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
            self.mentor != self.mentee,
            not self.match_count('mentor', 'no'),
            True if self.match_type == 'preferred' else not self.match_count('mentee', 'no'),
            True if self.match_type == 'preferred' else self.level_delta >= 0,
            True if self.match_type == 'preferred' else self.years_delta >= 0,
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
    def preferred(self):
        return self.match_type == 'preferred'

    @property
    def random(self):
        return self.match_type == 'random'

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


class PairComparison:

    def __init__(self, self_pair: Pair, other_pair: Pair):
        self.self_pair = self_pair
        self.other_pair = other_pair
        self.pairs = [self_pair, other_pair]

    def get_better_pair(self) -> bool:

        # if not self.self_pair.compatible:
        #     return False
        # elif not self.other_pair.compatible:
        #     return True

        # else...

        # TODO preferred comparison
        if self.self_pair.preferred and self.other_pair.random:
            return self.self_pair
        elif self.self_pair.random and self.other_pair.preferred:
            return self.other_pair
        if self.self_pair.preferred and self.self_pair.preferred:
            compare_funcs = [
                self.preferred_vs_random,
                self.location_and_gender_mentor,
                self.level_delta,
                self.years_delta,
                self.rank_order,  # Preferred Only
                self.wwid_count,  # Preferred Only
                self.hashorder,
            ]
        elif self.self_pair.random and self.self_pair.random:
            compare_funcs = [
                self.preferred_vs_random,
                self.location_and_gender_mentor,
                self.location_and_gender_mentee,  # Random only
                self.level_delta,
                self.years_delta,
                self.hashorder,
            ]
        else:
            raise ValueError

        ###################
        # Favored Mentees #
        ###################
        max_restart_count = max(pair.mentee.restart_count for pair in self.pairs)
        # TODO max restart needs to reset when switching over to random pairing.
        insert_index = -(1 + max_restart_count)  # always occurs before hashorder, an unfair arbitrary metric
        insert_index = max(len(compare_funcs), insert_index)  # make sure it's never out of range
        compare_funcs.insert(insert_index, self.favored)

        for func in compare_funcs:
            better_pair = func()
            if better_pair is PairsEqual:
                # It's a tie. Go to next comparison function
                continue
            else:
                return better_pair
        raise ValueError("One of these pairs should have been better than the other!")  # pragma: no cover

    def get_true(self):
        return True

    def _better_pair(self, _list, min_mode=False):
        if _list[0] == _list[1]:
            return PairsEqual
        minmax_func = min if min_mode else max
        best_index = _list.index(minmax_func(_list))
        return self.pairs[best_index]

    def preferred_vs_random(self):
        scoring = {'preferred': 1, 'random': 0}
        scores = [
            scoring[pair.match_type]
            for pair in self.pairs
        ]
        better_pair = self._better_pair(scores)
        return better_pair

    def location_and_gender_mentee(self):
        return self._location_and_gender('mentee')

    def location_and_gender_mentor(self):
        return self._location_and_gender('mentor')

    def _location_and_gender(self, chooser):
        # Assumption: both mentees have already passed the compatible test
        # The mentee who has more "yeses" wins.
        # If tied, then the mentee with more "maybes" wins.

        for pref_suffix in "yes maybe".split():
            scores = [
                pair.match_count(chooser, pref_suffix)
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
