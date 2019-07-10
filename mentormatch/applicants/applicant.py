from bin.schema.schema import Schema


class Applicant:

    def __init__(self, applicant_data, applicant_group):
        fields = Schema.get_fields_namedtuple(applicant_group)
        self.data = fields(**applicant_data)
        self.__applicant_group = applicant_group

    @property
    def applicant_group(self):
        return self.__applicant_group

    def get_full_name(self):
        full_name = ' '.join([self.data.first_name, self.data.last_name])
        return full_name.strip()

    def is_same_person_as(self, other):
        # This is used in case a person applied more than once.
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.data.wwid == other.data.wwid

    def __str__(self):
        return f'WWID: {self.data.wwid}\t Name: {self.get_full_name()}'

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

    def get_variable_data(self):
        # TODO bad function get_name
        # TODO pseudocode
        #   experience years
        #   genders
        #   sites
        #   check the Schema for full list
        pass


if __name__ == '__main__':
    pass
