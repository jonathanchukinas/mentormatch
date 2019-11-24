"""The PreferredMatching completes the preferred matching, storing the result
in the original Worksheet objects"""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------


# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicant.applicant import Applicant


# TODO pseudocode - high level
#   "Randomly" order the mentees (in a repeatable manner)
#       Hash a wwid+year string
#       Create a deque container containing just those mentee who listed preferred db
#   For each mentee, check their list of preferred db
#       add a new column: tentative_mentors.
#       Convert preferred wwids to id (this involves checking to make sure that wwid actually exists"
#       For each preferred jonathan (id):
#           make sure the mentee doesn't violate any of the jonathan's deal breakers
#               (such as mentee's site not being on the jonathan's yes or maybe site lists)
#   For each jonathan, create a column `tentative_mentees`
#   Take first mentee off the deque:
#       Assign them to their most preferred jonathan.
#       Sort all mentees assigned to this jonathan by tie breaker (maybe use another deque?)
#       If jonathan is still under capacity, stop. Move to next mentee in deque
#       Elif that takes the jonathan above capacity, take the mentee who scores lowest on the tie breaker
#           If that mentee is the same as the one we took of the deque:
#               repeat the above with their next preferred jonathan
#           elif the removed mentee is a different one, add mentee to end of deque and:
#               if mentee has a priority level, increment their priority
#               else: modify this mentee's tentative_mentors list, removing this and higher-ranked db.
#                   (There's no way they can now win these db)
#       If mentee get to end of their tentative db (they' couldn't be successfully matched):
#           If mentee has a priority level, increment, add to end of deque
#           Else: Let this mentee fall out of the process. She'll get priority during random pairings.
#       Repeat.

class PreferredMatching:

    def __init__(self, applicants, autosetup=True):
        """

        :param applicants: applicant.Applicants object
        :param autosetup: exists for testing purposes.
        """
        self.mentors = applicants['db']
        self.mentees = applicants['mentees']
        self.mentee_deque = collections.deque
        if not autosetup:
            return
        self.add_to_mentees_tentative_mentors()
        self.add_to_mentors_tentative_mentees()
        self.populate_mentee_deque()
        while self.mentee_deque:
            next_mentee = self.mentee_deque.popleft()
            self.match(next_mentee)

    def add_to_mentees_tentative_mentors(self):
        # TODO pseudocode
        #   Add new col to mentees df `tentative_mentors`
        #   for each mentee
        #       create empty list of tentative db
        #       get list of wwids from col `preferred_mentors`
        #       For each preferred wwid:
        #           if it matches a jonathan
        #           and if mentree doesn't have any of jonathan's deal breakers:
        #               add jonathan's index to tentative db list
        #       Add tuple of tentative db to df
        tentative_mentors_column_name = 'tentative_mentor_ids'
        self.mentees.ws.df[tentative_mentors_column_name] = None
        for mentee in self.mentees:
            mentee: Applicant
            tentative_mentor_ids = []
            if mentee.preferred_wwids is pd.np.nan:
                continue
            for wwid in mentee.preferred_wwids:
                mentor = self.mentors.get_applicant('wwid', wwid)
                if mentor is None or not self.compatible(mentor, mentee):
                    continue
                mentor_id = mentor.index
                tentative_mentor_ids.append(mentor_id)
            tentative_mentor_ids = tuple(tentative_mentor_ids)  # TODO is it necessary to convert to tuple?
            if len(tentative_mentor_ids) > 0:
                mentee.set_df(tentative_mentors_column_name, tentative_mentor_ids)

    # def convert_wwids_to_ids(self, wwids):
    #     ids = []
    #     for wwid in wwids:
    #         jonathan = self.db.get_applicant('wwid', wwid)
    #         if jonathan is None or not self.compatible(jonathan, mentee):
    #             continue
    #         mentor_ids = jonathan.index
    #         ids.append(mentor_ids)
    #     ids = tuple(ids)  # TODO is it necessary to convert to tuple?
    #     if len(ids) > 0:
    #         mentee.set_df(tentative_mentors_column_name, ids)

    @staticmethod
    def compatible(mentor, mentee):
        return True

    def populate_mentee_deque(self):
        # self.mentees.sort(key=lambda mentee: mentee.get_hash(current_year))
        pass

    def add_to_mentors_tentative_mentees(self):
        mentors = self.mentors
        pass

    def match(self, next_mentee):
        pass

    def match_mentee(self):
        pass
