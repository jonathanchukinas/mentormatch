from contextlib import contextmanager


current_mentor = None


def better_match(mentee1, mentee2):
    # TODO
    #   Mentor's site and gender pref
    #       The mentee with more "yes" wins.
    #       If tied on "yes", the mentee with more "maybe" wins.
    #   Level difference
    #       The mentee closer to the mentor's level wins
    #   Rank Order
    #       Whichever mentee ranked this mentor higher wins.
    #   WWID count
    #       The mentee with more preferred wwids wins.
    #   Favored
    #       The mentee who is more favored (b/c e.g. has been more often or more recently rejected) wins.
    #       **This will move up in importance as the mentee gets fails to pair with one of her preferred mentors.**
    #   Early bird
    #       The mentee who applied first wins
    pass


def mentor_pref_yes(mentee1, mentee2):

    # TODO pseudocode
    #   get the mentor's "yes" sites.
    #   get the mentor's "yes" genders.
    #
    pass


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
# TODO make sure the above accounts for "favored" status.


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
    current_mentor = mentor
    yield
    current_mentor = None


#
# def get_current_mentor():
#     return current_mentor
