
# Tiebreakers
# TODO pseudocode
#   This serves mostly (only?) to compare one potentially pairing with another.
#   Comparisons are based on:
#   Ties are broken in the following order (starting with the first):
#       1 - Mentor preferences (site, gender). A mentee who has more "yes"es break the tie.
#       2 - Level difference: A smaller level difference wins.
#       3 - Rank Order: Whichever mentee ranked this jonathan higher wins.
#       4 - Count of preferred wwids: The mentee who listed more preferred wwids wins.
#       5 - History - the mentee who's been rejected the most or had the least number of db wins
#       6 - Priority - mentees who were rejected last year fall into this category.
#               These are the ones we want badly to match up this year.
#               This one has the potential to move up the tiebreaker order.
#               If, for example, we arrive at the end and there are 'priority' mentees
#       7 - First applied - probably will only rarely come up, but there needs to be some final tie breaker...
#   There are other factors I brainstormed, but they won't be used during the preferred matching phase.
#       Random vs. Preferred Pairing -- not used in preferred matching
#       Does the Mentee want a random pairing at all? -- not used in preferred matching
#       Mentee preferences (site, gender)  -- not used in preferred matching

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
    return True
