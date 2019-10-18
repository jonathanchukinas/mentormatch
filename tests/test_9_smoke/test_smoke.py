# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pytest

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.main import api


# @pytest.mark.skip()
def test_smoke(test_path):
    api.main(test_path)
