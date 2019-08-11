


class MentorWrapper(ApplicantWrapper):

    def __init__(self, applicant):
        super().__init__(applicant)
        self.__tentative_mentees = []
        self.__committed_mentees = []

    def add_mentee(self, mentee):
        self.__tentative_mentees.append(mentee)
        ##
        #
        #
        return None # or the rejected mentee


class MenteeWrapper(ApplicantWrapper):

    def __init__(self, applicant):
        super().__init__(applicant)
        self.__matched = False
        self.__rejection_count = 0

    def still_unmatched(self):
        return self.__matched

    def mark_as_matched(self):
        self.__matched = True

    def could_not_find_a_match(self):
        self.__rejection_count += 1
        # TODO adjust the "priority" tie breaker to be more favorable for this mentee.

    def still_has_chances(self):
        if self.__rejection_count < 6
