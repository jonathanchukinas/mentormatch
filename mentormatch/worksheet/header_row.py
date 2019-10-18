"""These functions related to the pandas dataframe extracted from
the procedure-based requirements excel worksheet."""

# --- Standard Library Imports ------------------------------------------------
from difflib import SequenceMatcher
import statistics

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
import xlrd

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main.exceptions import MentormatchError


def find_most_similar_string(value: str, strings: list, return_ratio=False):
    """Return the best match to a given string."""
    string = str(value)
    if len(strings) == 0:
        if return_ratio:
            return 0
        else:
            return None
    ratios = [
        SequenceMatcher(None, string, str(orig_string)).ratio()
        for orig_string in strings
    ]
    max_ratio = max(ratios)
    if return_ratio:
        return max_ratio
    else:
        index = ratios.index(max_ratio)
        return strings[index]


def map_one_string_to_another(expected_strings: set, actual_strings: set):
    """
    Maps field names to their exact or best matches in pandas dataframe.
    :param expected_strings: strings for whom we seek the best match
    :param actual_strings: available strings
    :return: dict[expected_string] = actual_string
    """

    # --- Setup ---------------------------------------------------------------
    result = {}

    # --- Get exact matches ---------------------------------------------------
    for string in expected_strings & actual_strings:
        result[string] = string
    remaining_expected = list(expected_strings - actual_strings)
    remaining_actual = list(actual_strings - expected_strings)

    # --- Order expected strings by best match --------------------------------
    def sort_by_match_ratio_then_alphbetical(input_string):
        ratio = find_most_similar_string(
            value=input_string,
            strings=list(remaining_expected),
            return_ratio=True,
        )
        return ratio, input_string
    remaining_expected.sort(key=sort_by_match_ratio_then_alphbetical)

    # --- Find best match for each remaining string ---------------------------
    for string in remaining_expected:
        best_actual = find_most_similar_string(string, remaining_actual)
        result[string] = best_actual
        if best_actual is not None:
            remaining_actual.remove(best_actual)

    # --- Return result -------------------------------------------------------
    return result


def similarity_between_two_strings(input_strings, output_strings):
    match_ratios = [find_most_similar_string(string, output_strings, True) for string in input_strings]
    return statistics.mean(match_ratios)


def find_header_row(excel_path, excel_sheet_name, headers_list):

    # --- Get dataframe -------------------------------------------------------
    try:
        df = pd.read_excel(
            io=excel_path,
            sheet_name=excel_sheet_name,
            header=None,
            dtype=object,
        )
    except FileNotFoundError:
        raise MentormatchError(f'<{excel_path}> not valid file.')
    except xlrd.biffh.XLRDError:
        raise MentormatchError(f"<{excel_sheet_name}> sheet not found")

    # --- get list of first 20 rows -------------------------------------------
    rows = []
    for row_index, row in enumerate(df.itertuples()):
        if row_index == 20:
            break
        row_values = list(df.iloc[row_index])
        rows.append(row_values)

    # --- find best matching row ----------------------------------------------
    similarities = [similarity_between_two_strings(headers_list, row) for row in rows]
    best_match = max(similarities)
    best_match_row_index = similarities.index(best_match)
    return best_match_row_index + 1


if __name__ == '__main__':
    headers = 'hello good bye'.split()
    actual = ['hello', 'good', 'bye', 'bye']
    print(similarity_between_two_strings(headers, actual))
