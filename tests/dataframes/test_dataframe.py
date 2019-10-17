# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from rtm.containers import dataframe


def test_find_best_match():
    input_string = 'apple'
    strings = 'banana apl cherry'.split()
    assert dataframe.find_best_match(input_string, strings, True) > 0.5
    assert dataframe.find_best_match(input_string, strings) == 'apl'


def test_map_expected_to_actual():
    expected = {
        # 'ID',
        # 'Procedure Step',
        # 'Need',
        # 'Design Input',
        'Solution Level 1',
        'Solution Level 2',
        'Solution Level 3',
        'Solution Level 4',
        'Solution Level 5',
        'Solution Level 6',
        'Solution Level 7',
        # 'Cascade Level',
        # 'Requirement Statement',
        # 'Requirement Rationale',
        # 'Verification or Validation Strategy',
        # 'Verification or Validation Results',
        # 'Devices Design Output Feature (with CTQ ID #)',
        # 'CTQ? Yes, No, N/A',
    }

    actual = {
        # 'ID',
        # 'Procedure Step',
        # 'Need',
        # 'Design Input',
        'Solution Level 1',
        'SolutionLevel 2',
        'Solution Level  3',
        # 'Cascade Level',
        # 'Requirement Statement',
        # 'Requirement Rationale',
        # 'Verification or Validation Strategy',
        # 'Verification or Validation Results',
        # 'Devices Design Output Feature (with CTQ ID #)',
        # 'CTQ?\nYes, No, N/A',
    }

    expected_result = dict()
    expected_result['Solution Level 1'] = 'Solution Level 1'
    expected_result['Solution Level 2'] = 'SolutionLevel 2'
    expected_result['Solution Level 3'] = 'Solution Level  3'
    expected_result['Solution Level 4'] = None
    expected_result['Solution Level 5'] = None
    expected_result['Solution Level 6'] = None
    expected_result['Solution Level 7'] = None

    actual_result = dataframe.map_expected_to_actual(expected, actual)
    assert actual_result == expected_result
