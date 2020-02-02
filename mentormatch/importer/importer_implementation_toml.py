from __future__ import annotations
from .importer_abc import Importer
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType
    from pathlib import Path


class ImporterToml(Importer):

    def __init__(self, path: Path):
        self._path = path

    def execute(self) -> Dict[ApplicantType, List[Dict]]:
        raise NotImplementedError
