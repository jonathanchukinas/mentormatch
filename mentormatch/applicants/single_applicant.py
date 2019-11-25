"""The Applicant object represents a single applicant. It stores very little
data on its own. It has access to a Worksheet object"""

# --- Standard Library Imports ------------------------------------------------
import hashlib

from unittest.mock import sentinel  # https://www.revsys.com/tidbits/sentinel-values-python/

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


class SingleApplicant:

    group = None

    def __init__(self, db, doc_id, all_applicants):
        self.doc_id = doc_id
        self._all_applicants = all_applicants
        self._db = db
        # hashable_string = (str(self.wwid) + str(self.worksheet.year)).encode()
        # self.hash = hashlib.sha1(hashable_string)  # Used for semi-random sorting

    def __eq__(self, other):
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.wwid == other.wwid

    def __str__(self):
        name = ' '.join([self.first_name, self.last_name]).strip()
        return f'WWID: {self.wwid}\t Name: {name}'

    def __getattr__(self, item):
        # TODO this needs to work the database
        df = self.worksheet.df
        row = df.iloc[self.index]
        try:
            return row[item]
        except KeyError:
            cls = type(self)
            msg = '{.__name__!r} object has no attribute {!r}'
            raise AttributeError(msg.format(cls, item))

    def set_df(self, column, value):
        df = self.worksheet.df
        row = df.iloc[self.index]
        try:
            row[column] = value
        except KeyError:
            cls = type(self)
            msg = '{.__name__!r} object has no attribute {!r}'
            raise AttributeError(msg.format(cls, column))

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
    #
    # # menteeonly
    # def ranking_of_this_mentor(self, jonathan):
    #     preferred_mentors = self.preferences.get('preferred_mentors', [])
    #     if isinstance(preferred_mentors, abc.Sequence):
    #         preferred_mentors.identification()
    #     else:
    #         return -1
    #

# TODO pseudocode - high level
#   "Randomly" order the mentees (in a repeatable manner)
#       Hash a wwid+year string
#       Create a deque container containing just those mentee who listed preferred mentors
#   For each mentee, check their list of preferred mentors
#       add a new column: tentative_mentors.
#       Convert preferred wwids to id (this involves checking to make sure that wwid actually exists"
#       For each preferred mentor (id):
#           make sure the mentee doesn't violate any of the mentor's deal breakers
#               (such as mentee's site not being on the mentor's yes or maybe site lists)
#   For each mentor, create a column `tentative_mentees`
#   Take first mentee off the deque:
#       Assign them to their most preferred mentor.
#       Sort all mentees assigned to this mentor by tie breaker (maybe use another deque?)
#       If mentor is still under capacity, stop. Move to next mentee in deque
#       Elif that takes the mentor above capacity, take the mentee who scores lowest on the tie breaker
#           If that mentee is the same as the one we took of the deque:
#               repeat the above with their next preferred mentor
#           elif the removed mentee is a different one, add mentee to end of deque and:
#               if mentee has a priority level, increment their priority
#               else: modify this mentee's tentative_mentors list, removing this and higher-ranked mentors.
#                   (There's no way they can now win these mentors)
#       If mentee get to end of their tentative mentors (they' couldn't be successfully matched):
#           If mentee has a priority level, increment, add to end of deque
#           Else: Let this mentee fall out of the process. She'll get priority during random pairings.
#       Repeat.

class Mentor(SingleApplicant):

    group = "mentors"

    def __init__(self, db, doc_id, all_applicants):
        super().__init__(db, doc_id, all_applicants)
        self._mentees = []

    def assign_mentee(self, mentee):
        self._mentees.append(mentee)
        # TODO sort by **DECREASING** match quality
        if len(self._mentees) > self.max_mentee_count:
            rejected_mentee = self._mentees.pop()
            self._all_applicants.mentees.queue.append(rejected_mentee)
            # TODO add weighting for preferred mentees?


NoMoreMentors = sentinel.NoMoreMentors


class Mentee(SingleApplicant):

    group = "mentees"

    def __init__(self, db, doc_id, all_applicants):
        super().__init__(db, doc_id, all_applicants)
        self.preferred_mentors = self.gen_preferred_mentors()

    def gen_preferred_mentors(self):
        for wwid in self.preferred_wwids:
            mentor = self._all_applicants.mentors[wwid]
            if mentor is None:
                continue
            yield mentor
        while True:
            yield NoMoreMentors

    def assign_to_preferred_mentor(self):
        mentor = next(self.preferred_mentors)
        if mentor is not NoMoreMentors:
            mentor.assign_mentee(self)
