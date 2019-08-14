from pathlib import Path
import pytest


@pytest.fixture(scope='session')
def test_path():
    return Path(__file__).parent / "test_mentormatch.xlsx"
