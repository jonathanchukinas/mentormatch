from mentormatch.schema.schema import Schema
import mentormatch.applicants.applicants as templates
import mentormatch.main.context_managers as context
import collections.abc as abc


class Applicant:

    def __init__(self, applicant_group):

        applicant_data = context.path.get()
        fields = Schema.get_fields_namedtuple(applicant_group)

        self.data = fields(**applicant_data)
        self.applicant_group = applicant_group

        if applicant_group == 'mentor':
            self.tentative_mentees = []
            self.committed_mentees = []
        if applicant_group == 'mentee':
            self.matched = False
            self.rejection_count = 0

    @property
    def name(self):
        full_name = ' '.join([self.data.first_name, self.data.last_name])
        return full_name.strip()

    def __eq__(self, other):
        # This is used in case a person applied more than once.
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.data.wwid == other.data.wwid

    def __str__(self):
        return f'WWID: {self.wwid}\t Name: {self.name}'

    def has_this_much_more_experience_than(self, other):
        # Mentees can only be paired with mentors who have more experience than them.
        years_diff = self.data.years - other.data.years
        level_diff = self.data.position_level - other.data.position_level
        if 0 < level_diff:
            return level_diff
        elif 0 == level_diff and 7 <= years_diff:
            return 0
        else:
            return -1

    # menteeonly
    def ranking_of_this_mentor(self, mentor):
        preferred_mentors = self.preferences.get('preferred_mentors', [])
        if isinstance(preferred_mentors, abc.Sequence):
            preferred_mentors.identification()
        else:
            return -1

    # menteeonly
    def could_not_find_a_match(self):
        self.rejection_count += 1
        # TODO adjust the "priority" tie breaker to be more favorable for this mentee.

    # menteeonly
    def still_has_chances(self):
        if self.rejection_count < 6:
            pass

    # mentoronly
    def add_mentee(self, mentee):
        if self.applicant_group != 'mentor':
            raise TypeError('add_mentee method can only be called by a mentor')
        self.__tentative_mentees.append(mentee)
        ##
        return None  # or the rejected mentee