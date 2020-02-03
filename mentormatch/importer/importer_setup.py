from __future__ import annotations
from fuzzytable import FuzzyTable, exceptions as fe
from .importer_implementation_excel_schema import fieldschemas, favor
from .importer_abc import Importer
from .importer_implementation_excel import ImporterExcel
from .importer_implementation_toml import ImporterToml
from typing import Dict, List, TYPE_CHECKING
import toml
from .util import get_path
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType
    from mentormatch.api.applicant import Mentor
    from pathlib import Path


class ImporterFactory:

    @staticmethod
    def select_file_dialog():
        return get_path()

    @staticmethod
    def get_exceltoml_importer(source_path: Path, save_path: Path) -> Importer:
        return _ImporterExcelToml(source_path, save_path)

    @staticmethod
    def get_toml_importer(source_path: Path) -> Importer:
        return ImporterToml(source_path)


class _ImporterExcelToml(Importer):

    def __init__(self, source_path: Path, save_dir: Path):
        self._source_path = source_path
        self._save_dir = save_dir
        self._save_dir.mkdir(exist_ok=True)
        self._save_path = save_dir / 'processed_applications.toml'
        self._save_path.touch()

    def execute(self) -> Dict[ApplicantType, List[Dict]]:

        # Import from Excel and save toml to disc
        importer_excel = ImporterExcel(self._source_path)
        application_dicts = importer_excel.execute()
        application_dicts = {
            key.lower(): value
            for key, value in application_dicts.items()
        }
        self._save_path.write_text(toml.dumps(application_dicts))
        del application_dicts

        # Import from toml and return
        importer_toml = ImporterFactory.get_toml_importer(
            source_path=self._save_path
        )
        application_dicts = importer_toml.execute()
        return application_dicts
