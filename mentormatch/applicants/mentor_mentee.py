from bin.applicants.applicant import Applicant


class MentorApplicant(Applicant):

    def __init__(self, applicant_data):
        super().__init__(applicant_data, 'mentors')


class MenteeApplicant(Applicant):

    def __init__(self, applicant_data):
        super().__init__(applicant_data, 'mentees')

    def ranking_of_this_mentor(self, mentor):
        if 'preferred_mentors' in self.preferences:
            preferred_mentors = self.preferences['preferred_mentors']
            if type(preferred_mentors) is list:
                preferred_mentors.identification()
        else:
            return -1
