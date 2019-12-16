from contextlib import contextmanager
from mentormatch.schema.fieldschema import locations, genders
from typing import List
from collections import Counter

current_mentor = None
mentees = []


# TODO is this func needed? Remove?
def worse_match(mentee1, mentee2):
    better_mentee = better_match(mentee1, mentee2)
    mentees.remove(better_mentee)
    return mentees[0]


def better_match(mentee1, mentee2):
    if current_mentor is None:
        raise NotImplementedError("current_mentor has not been initialized yet.")
    global mentees
    mentees = mentee1, mentee2

    compare_funcs = [
        location_and_gender,
        level_delta,
        years_delta,
        rank_order,
        wwid_count,
        # 'Early Bird' not implemented
        hashorder,
    ]
    ###################
    # Favored Mentees #
    ###################
    max_restart_count = max(mentee.restart_count for mentee in mentees)
    insert_index = -(1+ max_restart_count)  # always occurs before hashorder, an unfair arbitrary metric
    insert_index = max(len(compare_funcs), insert_index)  # make sure it's never out of range
    compare_funcs.insert(insert_index, favored)

    for func in compare_funcs:
        better_mentee = func()
        if better_mentee is not None:
            return better_mentee


def location_and_gender():
    # The mentee who has more "yeses" wins.
    # If tied, then the mentee with more "maybes" wins.
    for pref_level in "yes maybe".split():
        pref_matches = [0] * len(mentees)
        for pref_category in "genders locations".split():
            mentor_pref = getattr(getattr(current_mentor, pref_category), pref_level)
            for index, mentee in enumerate(mentees):
                if getattr(mentee, pref_category).self in mentor_pref:
                    pref_matches[index] += 1
        best_mentee = get_best_mentee(pref_matches, 'max')
        if best_mentee is not None:
            return best_mentee
    return None


def level_delta():
    # The mentee closer to the mentor's level wins
    mentor_level = current_mentor.position_level
    deltas = [
        mentor_level - mentee.position_level
        for mentee in mentees
    ]
    return get_best_mentee(deltas, 'min')


def years_delta():
    # The mentee closer to the mentor's level wins
    mentor_years = current_mentor.years_total
    deltas = [
        mentor_years - mentee.years_total
        for mentee in mentees
    ]
    return get_best_mentee(deltas, 'min')


def rank_order():
    # Whichever mentee ranked this mentor higher wins.
    mentor_wwid = current_mentor.wwid
    ranking = [
        mentee.preferred_mentors.index(mentor_wwid)
        for mentee in mentees
    ]
    return get_best_mentee(ranking, 'min')


def wwid_count():
    # The mentee with more preferred wwids wins.
    wwid_counts = [
        len(mentee.preferred_mentors.index)
        for mentee in mentees
    ]
    return get_best_mentee(wwid_counts, 'max')


def get_best_mentee(_list, min_or_max):
    score_counter = Counter(_list)
    if min_or_max == 'min':
        best_score = min(score_counter)
    elif min_or_max == 'max':
        best_score = max(score_counter)
    else:
        raise ValueError
    if 1 == score_counter[best_score]:
        best_index = _list.index(best_score)
        return mentees[best_index]
    return None


def favored():
    #       The mentee who is more favored (b/c e.g. has been more often or more recently rejected) wins.
    #       **This will move up in importance as the mentee fails to pair with one of her preferred mentors.**
    # TODO implement "favored" attribute
    if mentees[0].favored > mentees[1].favored:
        return mentees[0]
    elif mentees[0].favored < mentees[1].favored:
        return mentees[1]
    else:
        return None


def hashorder():
    hashes = [
        (mentee, mentee.hash)
        for mentee in mentees
    ]
    best_mentee = max(hashes, key=lambda m: m[1])
    return best_mentee[0]


# TODO: experience level
# def has_this_much_more_experience_than(self, other):
#     # Mentees can only be paired with db who have more experience than them.
#     years_diff = self.get('years') - other.get('years')
#     level_diff = self.data.position_level - other.data.position_level
#     if 0 < level_diff:
#         return level_diff
#     elif 0 == level_diff and 7 <= years_diff:
#         return 0
#     else:
#         return -1


def compatible(mentor, mentee):
    # TODO implement
    # TODO make sure previous pairs don't get paired again
    return True


# class CurrentMentor:
#
#     def __init__(self):
#         self.mentor = None
#
#     def set_mentor(self, mentor):
#         self.mentor = mentor

@contextmanager
def set_current_mentor(mentor):
    global current_mentor
    global mentees
    current_mentor = mentor
    yield
    current_mentor = None
    mentees = None


#
# def get_current_mentor():
#     return current_mentor

if __name__ == '__main__':
    _list = list(range(5))
    _list.insert(-5, 99)
    print(_list)
