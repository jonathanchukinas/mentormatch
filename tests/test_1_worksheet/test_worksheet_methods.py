# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.worksheet.worksheet import Worksheet


def test_add_rows(test_path):
    ws = Worksheet(test_path, 'test_index_names')
    ws.add_row_column()
    df = ws.df
    expected_rows = [2, 3, 4, 5]
    actual_rows = list(df['row'])
    assert actual_rows == expected_rows
    assert df['row'].dtype == int


def test_drop_dups(test_path):
    pass


# TODO test for when a worksheet is missing a header
