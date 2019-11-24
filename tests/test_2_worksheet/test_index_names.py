# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pandas as pd
nan = pd.np.nan

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.worksheet.worksheet import Worksheet
from mentormatch import config


def empty_converter(value):
    return value


converters = {
    'wwid': empty_converter,
    'first_name': empty_converter,
}


def test_names(fixture_path):
    """Dataframe should only save those columns passed as keys to converters"""

    # --- get dataframe -------------------------------------------------------
    df = Worksheet(fixture_path, 'test_index_names', converters=converters).df
    print()
    print(df)

    # --- compare -------------------------------------------------------------
    expected_headers = set(converters.keys())
    actual_headers = set(df.columns)
    assert actual_headers == expected_headers
