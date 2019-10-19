"""This module defines the fields that the mentors and mentees worksheets
should contain."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import config
from mentormatch.worksheet import validation as v


FieldValidation = collections.namedtuple(
    'FieldValidation',
    [
        'name',  # Header name
        'val_func',  # validation function. default: `convert_string`
        'mentor_only',  # Does this field apply only to mentors? default: False
        'mentee_only',  # Does this field apply only to mentees? default: False
        'index_field',  # Is this an index field? i.e. Can a row be accessed with this field, like a dict?
        'post_dtype',  # Apply this dtype to the field after importing from excel.
                        # This gives the app a chance to raise an error if data is missing.
                        # Example: wwid has a post_dtype of int. If there are any missing values in the excel sheet,
                        # an error will be thrown. If no missing values, ....
                        # TODO check the above statements.
        'error_txt',
    ],
)
FieldValidation.__new__.__defaults__ = (None, v.convert_string, False, False, False, None, None)
f = FieldValidation


schema = [

    # Identification
    f('first_name'),
    f('last_name'),
    f('wwid', v.convert_integer, index_field=True, error_txt="This cell requires an integer."),

    # Biography
    f('gender'),
    f('site'),
    f('position_level', v.convert_first_digit_bw_2_6),
    f('years', v.convert_float),

    # Preferences
    f('genders_yes', v.convert_tuple_words),
    f('genders_maybe', v.convert_tuple_words),
    f('sites_yes', v.convert_tuple_words),
    f('sites_maybe', v.convert_tuple_words),
    f('max_mentee_count', v.convert_integer, mentor_only=True),
    f('preferred_wwids', v.convert_tuple_ints, mentee_only=True),
    f('wants_random_mentor', v.convert_boolean, mentee_only=True),

    # History
    f('application_years', v.convert_tuple_ints, mentee_only=True),
    f('participation_years', v.convert_tuple_ints, mentee_only=True),
]

schemas = {
    'mentors': [field for field in schema if not field.mentee_only],
    'mentees': [field for field in schema if not field.mentor_only]
}

converters = dict()
for group in config.groups:
    schema = schemas[group]
    fields = {field.name: field.val_func for field in schema}
    converters[group] = fields


if __name__ == '__main__':
    pass
