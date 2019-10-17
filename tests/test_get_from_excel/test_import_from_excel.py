# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
import pytest

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.get_from_excel import header_row, get_dataframe, schema


def test_most_similar_string():
    input_string = 'apple'
    strings = 'banana apl cherry'.split()
    assert header_row.find_most_similar_string(input_string, strings, True) > 0.5
    assert header_row.find_most_similar_string(input_string, strings) == 'apl'


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

    actual_result = header_row.map_one_string_to_another(expected, actual)
    assert actual_result == expected_result


def test_find_header_row(test_path):
    header_row_expected = 4
    header_row_actual = header_row.find_header_row(test_path, 'find_header_row', 'apples grapes'.split())
    assert header_row_actual == header_row_expected


def test_converters(test_path):

    converters_and_expected_results = dict()

    CheckSet = collections.namedtuple("CheckSet", "converter expected_values pytest_approx")
    CheckSet.__new__.__defaults__ = (None, None, False)

    converters_and_expected_results['string'] = CheckSet(
        schema.convert_string,
        [
            '1',
            'False',
            'True',
            '1',
            'hello',
            pd.np.nan,
            'two spaces left',
            'two spaces right',
        ]
    )

    converters_and_expected_results['list_of_words'] = CheckSet(
        schema.convert_tuple_words, [
            ('1',),
            ('False',),
            ('True',),
            ('1',),
            ('hello',),
            pd.np.nan,
            ('hello', 'good', 'bye'),
            ('123', '456', '78hi'),
        ]
    )

    converters_and_expected_results['first_digit'] = CheckSet(schema.convert_first_digit, [
        # 2,
        # # 0,
        # # 0,
        # # 0,
        # # 0,
        # # 0,
        # pd.np.nan,
        # pd.np.nan,
        # pd.np.nan,
        # pd.np.nan,
        # pd.np.nan,
        # 3,
        # 2,
        2,
        # 0.0,
        # 0.0,
        # 0.0,
        # 0.0,
        # 0.0,
        pd.np.nan,
        pd.np.nan,
        pd.np.nan,
        pd.np.nan,
        pd.np.nan,
        3.0,
        2.0,
    ], True)

    # --- get dataframe -------------------------------------------------------
    converters = {
        header: check_set.converter
        for header, check_set in converters_and_expected_results.items()
    }
    df = get_dataframe.get_df(test_path, 'test_converters',converters=converters)
    print(df)

    # --- compare -------------------------------------------------------------
    for header, check_set in converters_and_expected_results.items():
        if check_set.pytest_approx:
            expected_values = pytest.approx(check_set.expected_values, nan_ok=True)
        else:
            expected_values = check_set.expected_values
        actual_values = list(df[header])
        assert actual_values == expected_values


if __name__ == '__main__':
    pass
