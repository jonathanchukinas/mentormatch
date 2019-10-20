# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.worksheet import header_row


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


def test_find_header_row(fixture_path):
    header_row_expected = 4
    header_row_actual = header_row.find_header_row(fixture_path, 'get_header_row_number', 'apples grapes'.split())
    assert header_row_actual == header_row_expected
