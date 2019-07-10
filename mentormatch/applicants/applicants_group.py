from bin.applicants.mentor_mentee import MentorApplicant, MenteeApplicant


class ApplicantsGroup:
    """Objects of this class will house either all mentors or all mentees"""

    def __init__(self, worksheet_, applicant_group):
        self.__worksheet = worksheet_
        self.__applicant_group = applicant_group

    def generate_unique_applicants(self):
        applicants = [self.__generate_applicant(row_) for row_ in self.__worksheet]
        unique_wwids = set([applicant.data.wwid for applicant in applicants])
        unique_applicants = []
        for wwid in unique_wwids:
            applicants_with_this_wwid = [applicant for applicant in applicants if applicant.data.wwid == wwid]
            most_recent_of_these_applicants = self.__get_most_recent_applicant(applicants_with_this_wwid)
            unique_applicants.append(most_recent_of_these_applicants)
        return unique_applicants

    def __generate_applicant(self, row_):
        available_classes = {'mentors': MentorApplicant,
                             'mentees': MenteeApplicant}
        applicant_class = available_classes[self.__applicant_group]
        applicant = applicant_class(row_)
        return applicant

    @staticmethod
    def __get_most_recent_applicant(applicants):
        # TODO need to code this
        #   for now, I'll just return the first
        return applicants[0]

    def log_report(self):
        # TODO pseudocode
        #   for each mentor/ee
        #       collect all values from these 'keys':
        #           sites, gender, etc...
        #           store counter of each (e.g. I want to know how many times Fort Washington appears
        #   (use counters) https://docs.python.org/2/library/collections.html#collections.Counter
        pass
