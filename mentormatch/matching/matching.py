from mentormatch.applicants import AllApplicants

class Matching:

    def __init__(self, applicants: AllApplicants):
        self.applicants = applicants

    def random_matching(self):
        # TODO Pseudocode
        #   Create queue of mentees who didn't rcv preferred mentor
        #   Create queue of mentors who still have capacity
        #   for each seeking mentee:
        #       Yield next best-match mentor
        #       Add to mentor IF that pair is than one that would be rejected.
        #       Either way, if a mentee is rejected, put them at the end of the queue.
        # TODO: a preferred pair auto-trumps a random pair
        # TODO new tie-breaker: number of pairs the mentor has (obviously a tie if mentor is same person)

        # TODO pair comparisons:
        # Compatibility
        #   years delta
        #   experience delta
        #   location/gender no
        # Mentor-first:
        #   Mentor gets at least one mentee
        #   Reduce mentee count
        #       The previous two are problematic b/c they change as mentees get assigned.
        #       Should not be used for determining mentee's mentor queue
        #       I don't think it should be used....
        #   Increase mentor yes'es
        #   Increase mentor maybe's
        # Mentees who requested a preferred mentor
        #   mentee who added preferred wwids trumps one who did not.
        # Maximize pairings:
        #   decrease years delta
        #   decrease exp delta
        # Mentee-second
        #   yes   count: location/gender + match count: skills/department
        #   maybe count: location/gender + match count: skills/department
        #   or.... maybe combine the above two into a single value by halving the maybe count....

        # For each mentee, create a list of highest-quality pairs:
        #   compatible
        #   mentor: yes'es only
        #   mentee: yes'es only
        #   min 75% match in skills/department
        # Then, sort them in quality order

        # If that list gets exhausted, create a second list:
        #   not on previous list
        #   compatible
        #   mentor: yes'es only
        #   min 50% match in skills/dept

        # One penultimate list:
        #   not on previous lists
        #   compatible
        #   min 25% match in skills/dept

        # One last list:
        #   not on previous lists
        #   compatible
        pass
