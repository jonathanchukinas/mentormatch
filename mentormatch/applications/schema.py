# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from collections import namedtuple
import mentormatch.applications.validation_functions as v


FieldValidation = namedtuple('FieldValidation', 'name val_func mentor_only mentee_only')
FieldValidation.__new__.__defaults__ = (None, None, False, False)
f = FieldValidation

schema = [

    # Identification
    f('first_name'),
    f('last_name'),
    f('wwid', v.get_integer),

    # Biography
    f('gender'),
    f('site'),
    f('position_level', v.get_first_digit),
    f('years', v.get_float),

    # Preferences
    f('genders_yes', v.get_list_of_str),
    f('genders_maybe', v.get_list_of_str),
    f('sites_yes', v.get_list_of_str_csv),
    f('sites_maybe', v.get_list_of_str_csv),
    f('max_mentee_count', v.get_integer, mentor_only=True),
    f('preferred_wwids', v.get_list_of_ints, mentee_only=True),
    f('wants_random_mentor', v.get_boolean, mentee_only=True),

    # History
    f('application_years', v.get_list_of_ints, mentee_only=True),
    f('participation_years', v.get_list_of_ints, mentee_only=True),
]


def get_schema(group):
    if group == 'mentors':
        return [field for field in schema if not field.mentor_only]
    if group == 'mentees':
        return [field for field in schema if not field.mentee_only]


if __name__ == '__main__':
    FV = FieldValidation
    fv = FV('first_name', 'a func', mentee_only=True)
    print(fv)
    print()
    for item in schema:
        print()
        print(item)
