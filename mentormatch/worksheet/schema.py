"""This module defines the fields that the mentors and mentees worksheets
should contain, along with the functions that validate the incoming data."""

# --- Standard Library Imports ------------------------------------------------
import re
import collections
import datetime
import numbers

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
nan = pd.np.nan

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import config


def convert_integer(value):
    value_num = convert_float(value)
    if pd.isna(value_num):
        return nan
    return int(value)


def convert_float(value):
    if isinstance(value, bool):
        return nan
    if isinstance(value, numbers.Real):
        return float(value)
    return nan


def convert_boolean(value):
    if isinstance(value, bool):
        return value
    return nan


def convert_tuple_ints(value):
    value_string = convert_string(value)
    if pd.isna(value_string):
        return nan
    p = re.compile(r'\d+')  # Regular Expression for consecutive digits
    list_of_consecutive_digits = p.findall(value_string)
    tuple_ints = tuple([int(item) for item in list_of_consecutive_digits])
    if len(tuple_ints) == 0:
        return nan
    return tuple_ints


def convert_first_digit_bw_2_6(value):
    min_integer = 2
    max_integer = 6
    # first_integer = 0  # default value
    value_string = convert_string(value)
    if pd.isna(value_string):
        return nan
    pattern = f'[{min_integer}-{max_integer}]'
    p = re.compile(pattern)  # Regular Expression for individual digits
    list_of_individual_digits = p.findall(value_string)
    if len(list_of_individual_digits) > 0:
        first_digit = list_of_individual_digits[0]
        return int(first_digit)
    return pd.np.nan


def convert_tuple_words(value):
    """get a list of alphanumeric sequences"""
    value_string = convert_string(value)
    if pd.isna(value_string):
        return nan
    p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
    words = tuple(p.findall(value_string))
    if len(words) == 0:
        return nan
    return words


def convert_string(value):
    if isinstance(value, (bool, datetime.date, datetime.datetime)):
        return nan
    try:
        return str(value).strip()
    except TypeError:
        return nan


FieldValidation = collections.namedtuple(
    'FieldValidation',
    [
        'name',  # Header name
        'val_func',  # validation function. default: `convert_string`
        'mentor_only',  # Does this field apply only to mentors? default: False
        'mentee_only',  # Does this field apply only to mentees? default: False
        'index_field', # Is this an index field? i.e. Can a row be accessed with this field, like a dict?
        'post_dtype',  # Apply this dtype to the field after importing from excel.
                        # This gives the app a chance to raise an error if data is missing.
                        # Example: wwid has a post_dtype of int. If there are any missing values in the excel sheet,
                        # an error will be thrown. If no missing values, ....
                        # TODO check the above statements.
        'error_txt',
    ],
)
FieldValidation.__new__.__defaults__ = (None, convert_string, False, False, False, None, None)
f = FieldValidation


schema = [

    # Identification
    f('first_name'),
    f('last_name'),
    f('wwid', convert_integer, index_field=True, error_txt="This cell requires an integer."),

    # Biography
    f('gender'),
    f('site'),
    f('position_level', convert_first_digit_bw_2_6),
    f('years', convert_float),

    # Preferences
    f('genders_yes', convert_tuple_words),
    f('genders_maybe', convert_tuple_words),
    f('sites_yes', convert_tuple_words),
    f('sites_maybe', convert_tuple_words),
    f('max_mentee_count', convert_integer, mentor_only=True),
    f('preferred_wwids', convert_tuple_ints, mentee_only=True),
    f('wants_random_mentor', convert_boolean, mentee_only=True),

    # History
    f('application_years', convert_tuple_ints, mentee_only=True),
    f('participation_years', convert_tuple_ints, mentee_only=True),
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
    num = 1
    string = convert_string(num)
    print(string, type(string))
