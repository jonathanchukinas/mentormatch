import mentormatch.main.context_managers as context
import collections.abc as abc


class Applicant:

    def __init__(self, worksheet, index):

        self.index = index
        self.worksheet = worksheet

        # TODO: these should be added to the df itself
        group = worksheet.group
        if group == 'mentors':
            self.tentative_mentees = []
            self.committed_mentees = []
        if group == 'mentees':
            self.matched = False
            self.rejection_count = 0

    def __eq__(self, other):
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.wwid == other.wwid

    def __str__(self):
        name = ' '.join([self.first_name, self.last_name]).strip()
        return f'WWID: {self.wwid}\t Name: {name}'

    def __getattr__(self, item):
        df = self.worksheet.df
        row = df.iloc[self.index]
        try:
            return row[item]
        except KeyError:
            cls = type(self)
            msg = '{.__name__!r} object has no attribute {!r}'
            raise AttributeError(msg.format(cls, item))

    # def has_this_much_more_experience_than(self, other):
    #     # Mentees can only be paired with mentors who have more experience than them.
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
    # def ranking_of_this_mentor(self, mentor):
    #     preferred_mentors = self.preferences.get('preferred_mentors', [])
    #     if isinstance(preferred_mentors, abc.Sequence):
    #         preferred_mentors.identification()
    #     else:
    #         return -1
    #
    # # menteeonly
    # def could_not_find_a_match(self):
    #     self.rejection_count += 1
    #     # TODO adjust the "priority" tie breaker to be more favorable for this mentee.
    #
    # # menteeonly
    # def still_has_chances(self):
    #     if self.rejection_count < 6:
    #         pass
    #
    # # mentoronly
    # def add_mentee(self, mentee):
    #     if self.applicant_group != 'mentor':
    #         raise TypeError('add_mentee method can only be called by a mentor')
    #     self.__tentative_mentees.append(mentee)
    #     ##
    #     return None  # or the rejected mentee
