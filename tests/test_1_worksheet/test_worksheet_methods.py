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

    # indices
    # ( by "initial" I mean: following the removal of dups, but before reindexing)
    actual_initial_indices = list(ws.df.index.values)
    expected_initial_indices = [0, 1, 3]
    assert actual_initial_indices == expected_initial_indices
    ws.reset_index()
    actual_after_indices = list(ws.df.index.values)
    expected_after_indices = [0, 1, 2]
    assert actual_after_indices == expected_after_indices


def test_experiment_with_selecting_data(test_path):
    ws = Worksheet(test_path, 'drop_dups')
    ws.add_row_column()
    ws.drop_dups()
    df = ws.df
    print()
    first_row = df.iloc[0]
    print('first row:', first_row)

    column = 'first_name'
    print()
    print('column:', first_row[column])
