"""This module defines the fields that the mentors and mentees worksheets
should contain, along with the functions that validate the incoming data."""

# --- Standard Library Imports ------------------------------------------------
import re
from collections import namedtuple

# --- Third Party Imports -----------------------------------------------------
import pandas as pd

# --- Intra-Package Imports ---------------------------------------------------
# None


def get_integer(value):
    new_value = int()
    try:
        new_value = int(value)
    finally:
        return new_value


def get_float(value):
    new_value = float()
    try:
        new_value = float(value)
    finally:
        return new_value


def get_boolean(value):
    new_value = bool()
    try:
        new_value = bool(value)
    finally:
        return new_value


def get_list_of_ints(value):
    raw_data_as_string = convert_string(value)
    p = re.compile(r'\d+')  # Regular Expression for consecutive digits
    list_of_consecutive_digits = p.findall(raw_data_as_string)
    list_of_ints_ = [int(item) for item in list_of_consecutive_digits]
    return list_of_ints_


def convert_first_digit(value, min_integer=2, max_integer=6):
    # first_integer = 0  # default value
    raw_data_as_string = convert_string(value)
    pattern = f'[{min_integer}-{max_integer}]'
    p = re.compile(pattern)  # Regular Expression for individual digits
    list_of_individual_digits = p.findall(raw_data_as_string)
    if 0 < len(list_of_individual_digits):
        first_digit = list_of_individual_digits[0]
        return int(first_digit)
    return pd.np.nan


# def get_list_of_str_csv(value):
#     raw_data_as_string = convert_string(value)
#     list_of_words = raw_data_as_string.split(',')
#     list_of_words = [word.strip() for word in list_of_words]
#     return list_of_words


def convert_tuple_words(value):
    """get a list of alphanumeric sequences"""
    single_string = convert_string(value)
    p = re.compile(r'\w+')  # Regular Expression for consecutive alphabetical characters
    words = tuple(p.findall(single_string))
    if len(words) == 0:
        return pd.np.nan
    return words


def convert_string(value):
    # if isinstance(value, pd.np.nan):
    # # if value is pd.np.nan:
    #     return ''
    # new_value = str()
    # try:
    #     new_value = str(value).strip()
    # finally:
    #     return new_value
    return str(value).strip()


FieldValidation = namedtuple('FieldValidation', 'name val_func mentor_only mentee_only')
FieldValidation.__new__.__defaults__ = (None, convert_string, False, False)
f = FieldValidation


schema = [

    # Identification
    f('first_name'),
    f('last_name'),
    f('wwid', get_integer),

    # Biography
    f('gender'),
    f('site'),
    f('position_level', convert_first_digit),
    f('years', get_float),

    # Preferences
    f('genders_yes', convert_tuple_words),
    f('genders_maybe', convert_tuple_words),
    f('sites_yes', convert_tuple_words),
    f('sites_maybe', convert_tuple_words),
    f('max_mentee_count', get_integer, mentor_only=True),
    f('preferred_wwids', get_list_of_ints, mentee_only=True),
    f('wants_random_mentor', get_boolean, mentee_only=True),

    # History
    f('application_years', get_list_of_ints, mentee_only=True),
    f('participation_years', get_list_of_ints, mentee_only=True),
]


def get_schema(group):
    if group == 'mentors':
        return [field for field in schema if not field.mentor_only]
    if group == 'mentees':
        return [field for field in schema if not field.mentee_only]


if __name__ == '__main__':
    num = 1
    string = convert_string(num)
    print(string, type(string))
