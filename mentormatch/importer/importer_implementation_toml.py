from __future__ import annotations
from .importer_abc import Importer
from typing import Dict, List, TYPE_CHECKING
import toml
from mentormatch.utils import ApplicantType
if TYPE_CHECKING:
    from pathlib import Path


class ImporterToml(Importer):  # pragma: no cover

    def __init__(self, path: Path):
        self._path = path

    def execute(self) -> Dict[ApplicantType, List[Dict]]:
        _dict = toml.load(self._path)
        _dict = ApplicantType.convert_dict_keys_to_enum(_dict)
        return _dict
