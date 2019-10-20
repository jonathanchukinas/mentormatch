# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
import pytest
import pandas as pd

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import worksheet
from mentormatch.worksheet import validation as v


nan = pd.np.nan


def test_most_similar_string():
    input_string = 'apple'
    strings = 'banana apl cherry'.split()
    assert worksheet.header_funcs.find_most_similar_string(input_string, strings, True) > 0.5
    assert worksheet.header_funcs.find_most_similar_string(input_string, strings) == 'apl'


def test_map_one_string_to_another():
    expected = {
        'Solution Level 1',
        'Solution Level 2',
        'Solution Level 3',
        'Solution Level 4',
        'Solution Level 5',
        'Solution Level 6',
        'Solution Level 7',
    }

    actual = {
        'Solution Level 1',
        'SolutionLevel 2',
        'Solution Level  3',
    }

    expected_result = dict()
    expected_result['Solution Level 1'] = 'Solution Level 1'
    expected_result['Solution Level 2'] = 'SolutionLevel 2'
    expected_result['Solution Level 3'] = 'Solution Level  3'
    expected_result['Solution Level 4'] = None
    expected_result['Solution Level 5'] = None
    expected_result['Solution Level 6'] = None
    expected_result['Solution Level 7'] = None

    actual_result = worksheet.header_row.map_one_string_to_another(expected, actual)
    assert actual_result == expected_result


def test_find_header_row(fixture_path):
    header_row_expected = 4
    header_row_actual = worksheet.header_row.find_header_row(fixture_path, 'find_header_row', 'apples grapes'.split())
    assert header_row_actual == header_row_expected


def get_fields():
    _fields = dict()

    FieldParameters = collections.namedtuple(
        "FieldParameters",
        "converter expected_values pytest_approx, dtype, expected_dtype"
    )
    FieldParameters.__new__.__defaults__ = (None, None, False, None, None)

    _fields['string'] = FieldParameters(
        v.convert_string,
        [
            '1',
            nan,
            nan,
            '1',
            'hello',
            nan,
            'two spaces left',
            'two spaces right',
            nan,
        ],
        expected_dtype=object,
    )

    _fields['list_of_words'] = FieldParameters(
        expected_dtype=object,
        converter=v.convert_tuple_words,
        expected_values=[
            ('1',),
            nan,
            nan,
            ('1',),
            ('hello',),
            nan,
            ('hello', 'good', 'bye'),
            ('123', '456', '78hi'),
            nan,
        ],
    )

    _fields['first_digit'] = FieldParameters(
        converter=v.convert_first_digit_bw_2_6,
        expected_values=[
            2,
            4,
            6,
            4,
            3,
            5,
            3,
            2,
            3,
        ],
        expected_dtype='int64',
    )

    _fields['first_digit_missing'] = FieldParameters(
        converter=v.convert_first_digit_bw_2_6,
        expected_values=[
            2,
            nan,
            nan,
            nan,
            nan,
            nan,
            3.0,
            2.0,
            nan,
        ],
        pytest_approx=True,
        expected_dtype=float,
    )

    _fields['tuple_ints'] = FieldParameters(
        v.convert_tuple_ints, [
            (1,),
            nan,
            nan,
            (19, 3),
            nan,
            nan,
            (1, 2, 3),
            (20, 8),
            nan,
        ],
        expected_dtype=object,
    )

    _fields['boolean'] = FieldParameters(
        # dtype=bool,
        converter=v.convert_boolean,
        expected_values=[
            nan,
            False,
            True,
            nan,
            nan,
            nan,
            nan,
            nan,
            nan,
        ],
        expected_dtype=object,
    )

    _fields['boolean_perfect'] = FieldParameters(
        converter=v.convert_boolean,
        expected_values=[
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
        ],
        expected_dtype=bool,
    )

    _fields['all_numbers'] = FieldParameters(
        converter=v.convert_integer,
        expected_values=[
            1,
            2,
            3,
            465,
            77557357,
            12541,
            25,
            858,
            23,
        ],
        expected_dtype='int64',
    )

    _fields['ints_with_missing'] = FieldParameters(
        converter=v.convert_integer,
        pytest_approx=True,
        expected_values=[
            1.0,
            nan,
            nan,
            nan,
            nan,
            nan,
            25.0,
            858.0,
            nan,
        ],
        expected_dtype=float,
    )

    _fields['float'] = FieldParameters(
        converter=v.convert_float,
        pytest_approx=True,
        expected_values=[
            1.0,
            nan,
            nan,
            nan,
            nan,
            nan,
            25.5,
            858.0,
            nan,
        ],
        expected_dtype=float,
    )

    return _fields


fields = get_fields()
converters = {
    header: check_set.converter
    for header, check_set in fields.items()
}
headers = fields.keys()


def test_converters(fixture_path):

    # --- get dataframe -------------------------------------------------------
    df = worksheet.Worksheet(fixture_path, 'test_converters', converters=converters).df
    print()
    print(df)

    # --- compare -------------------------------------------------------------
    for header, parameters in fields.items():
        print()
        print('='*40)
        print()
        print(df[header])
        if parameters.pytest_approx:
            expected_values = pytest.approx(parameters.expected_values, nan_ok=True)
        else:
            expected_values = parameters.expected_values
        print()
        print('expected values:', expected_values)
        actual_values = list(df[header])
        print('actual values:  ', actual_values)
        assert actual_values == expected_values

        # check dtype
        expected_dtype = parameters.expected_dtype
        if expected_dtype is None:
            continue
        actual_dtype = df[header].dtype
        print('expected dtype:', expected_dtype)
        assert actual_dtype == expected_dtype


if __name__ == '__main__':
    pass
