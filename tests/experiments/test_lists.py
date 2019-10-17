# --- reversing and slicing lists -----------------------------------------


def slice_reverse_list(list_, count):
    return list_[: -(count + 1) : -1]


def test_slice_reverse_list():

    grape = list(range(1, 10))
    assert [9, 8, 7] == slice_reverse_list(grape, 3)

    banana = []
    assert [] == slice_reverse_list(banana, 1)

    melon = [1, 2]
    assert [2, 1] == slice_reverse_list(melon, 10)
