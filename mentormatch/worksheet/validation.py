"""These functions validate the incoming data from excel as it is saved to a
pandas dataframe."""

# --- Standard Library Imports ------------------------------------------------
import datetime
import numbers
import re

# --- Third Party Imports -----------------------------------------------------
import pandas as pd

# --- Intra-Package Imports ---------------------------------------------------
# None


nan = pd.np.nan


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
