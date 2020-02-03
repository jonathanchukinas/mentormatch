from __future__ import annotations
from .importer_abc import Importer
from typing import Dict, List, TYPE_CHECKING
import toml
from mentormatch.utils import ApplicantType
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType
    from pathlib import Path


class ImporterToml(Importer):

    def __init__(self, path: Path):
        self._path = path

    def execute(self) -> Dict[str, List[Dict]]:
        _dict = toml.load(self._path)
        return _dict
