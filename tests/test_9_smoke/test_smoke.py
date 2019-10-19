# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import api


# @pytest.mark.skip()
def test_smoke(fixture_path):
    api.main(fixture_path)
