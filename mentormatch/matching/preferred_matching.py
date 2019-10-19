"""The PreferredMatching completes the preferred matching, storing the result
in the original Worksheet objects"""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


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

class PreferredMatching:

    def __init__(self, applicants):
        self.mentors = applicants['mentors']
        self.mentees = applicants['mentees']
        self.mentee_deque = collections.deque
        self.add_to_mentees_tentative_mentors()
        self.add_to_mentees_hash()
        self.add_to_mentors_tentative_mentees()
        self.populate_mentee_deque()
        while self.mentee_deque:
            next_mentee = self.mentee_deque.popleft()
            self.match(next_mentee)

    def add_to_mentees_tentative_mentors(self):
        # add_to_mentees_tentative_mentors
        pass

    def add_to_mentees_hash(self):
        pass

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
