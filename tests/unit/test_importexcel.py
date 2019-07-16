from mentormatch import importexcel


def test_importexcel_reuse():
    assert "reuse" == importexcel(True, False)


def test_importexcel_new():
    # assert importexcel(False, True)
    assert isinstance(importexcel(False, True), str)


def test_importexcel_both():
    assert "select" == importexcel(True, True)


def test_importexcel_neither():
    assert "select" == importexcel(False, False)
