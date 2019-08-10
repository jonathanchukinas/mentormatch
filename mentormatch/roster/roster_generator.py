from collections import deque
import logging


# TODO I think I've wrtten tuples somewhere that use curly braces instaed of parentheses...


class RosterGenerator:
    """Collection for storing pairs of mentors and mentees."""

    def __init__(self, applicants):
        self.__ready = False
        self.__wrapped_applicants = self.__wrap_applicants(applicants)
        self.__roster = None

    def __wrap_applicants(self, applicants):
        # TODO
        #   wrap each applicant in their wrapper
        #       Mentors: stores matched mentees, func for available slots, etc
        #       Mentees: stores "is matched" boolean
        #   assign each applicant to a container
        self.__ready = True
        return 'Gotta put something meaningful here'

    def generate_roster(self):
        if self.__ready:
            self.__generate_preferred_matches()
            self.__generate_random_matches()
            return self.__roster

    def __generate_preferred_matches(self):

        # Randomize mentees with preferred wwids into a queue
        mentees = self.__mentees
        mentees = [mentee for mentee in mentees if mentee.has_preferred_mentors()]
        mentees.sort(key=lambda mentee: mentee.get_hash(current_year))
        mentee_queue = deque(mentees)
        del mentees

        while 0 < len(mentee_queue):
            mentee = mentee_queue.popleft()
            for wwid in mentee.preferred_wwids():
                mentor = self.__roster.get_applicant_by_wwid(wwid)
                rejected_mentee = mentor.add_mentee(mentee)
                if rejected_mentee is None:
                    # Success!
                    # Mentor still had capacity, therefore accepted this mentee
                    break
                elif rejected_mentee != mentee:
                    # Success!
                    # Mentor didn't have capacity, but this mentee was better than at least one of the
                    #   mentor's existing mentees. Put that rejected mentee at the end of the queue:
                    mentee_queue.append(rejected_mentee)
                    break
                elif rejected_mentee == mentee:
                    # Fail!
                    # Mentor didn't have capacity, and this mentee wasn't a good enough match to beat out the other(s)
                    #   already paired with this mentor.
                    pass
                else:
                    logging.debug('Mentor rejected something other than None, next_mentee, or this mentee')
            mentee.could_not_find_a_match()
            if mentee.still_has_chances():
                mentee_queue.append(mentee)
        pass

    def __generate_random_matches(self):
        pass

    def generate_report(self):
        # TODO - pseudocode - generate_report
        #   Accept a path to write the report to.
        #   If roster complete, generate report and save to output directory.
        #   Else, print error message
        pass
