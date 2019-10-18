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
    print(df)


def test_drop_dups(test_path):
    ws = Worksheet(test_path, 'drop_dups')
    # ws.add_row_column()

    # drop dups, checked dropped rows
    returned_dropped_rows = ws.drop_dups()  # which calls add_rows automatically
    expected_dropped_rows = [4, ]
    assert returned_dropped_rows == expected_dropped_rows

    # remaining rows
    actual_rows = list(ws.df['row'])
    expected_rows = [2, 3, 5]
    assert actual_rows == expected_rows


# TODO test for when a worksheet is missing a header
