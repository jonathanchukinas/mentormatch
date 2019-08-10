from bin.schema.data_field import DataField as df
from bin.schema.data_validation import DataTypeValidation as v
import logging
from collections import namedtuple


class Schema:
    applicant_groups = ['mentors', 'mentees']

    @classmethod
    def get_fields(cls, applicant_group='both'):
        """return list of DataField objects"""
        if applicant_group == 'both':
            return cls.__define_fields()
        elif applicant_group in cls.applicant_groups:
            return [field for field in cls.__define_fields() if field.applicable_to(applicant_group)]
        else:
            logging.debug(__name__, 'get_fields was passed a wrong applicant group:', applicant_group)

    @staticmethod
    def __define_fields():
        all_fields = [

            # Identification
            df('first_name'),
            df('last_name'),
            df('wwid', v.get_integer),

            # Biography
            df('gender'),
            df('site'),
            df('position_level', v.get_first_digit),
            df('years', v.get_float),

            # Preferences
            df('genders_yes', v.get_list_of_str),
            df('genders_maybe', v.get_list_of_str),
            df('sites_yes', v.get_list_of_str_csv),
            df('sites_maybe', v.get_list_of_str_csv),
            df('max_mentee_count', v.get_integer, applicant_group='mentors'),
            df('preferred_wwids', v.get_list_of_ints, applicant_group='mentees'),
            df('wants_random_mentor', v.get_boolean, applicant_group='mentees'),

            # History
            df('application_years', v.get_list_of_ints, applicant_group='mentees'),
            df('participation_years', v.get_list_of_ints, applicant_group='mentees'),
            # TODO add applicant date?
        ]
        return all_fields

    @classmethod
    def get_fields_namedtuple(cls, applicant_group):
        field_names_list = [str(field.get_name()) for field in cls.get_fields(applicant_group)]
        field_names_string = ' '.join(field_names_list)
        Fields = namedtuple('Fields', field_names_string)
        return Fields


if __name__ == '__main__':
    fields = Schema.get_fields()
    # field = fields[0]
    # print(field.get_name())
    field_names = [field.get_name() for field in fields]
    print(field_names)

