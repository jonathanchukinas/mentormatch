from __future__ import annotations
from fuzzytable import FuzzyTable, exceptions as fe
from .importer_implementation_excel_schema import fieldschemas, favor
from .importer_abc import Importer
from mentormatch.utils.exceptions import MentormatchError
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType


class ImporterExcel(Importer):

    def __init__(self, path):
        self._path = path

    def execute(self) -> Dict[ApplicantType, List[Dict]]:

        # For this to work, there needs to be one excel workbook with the following worksheets:
        # mentor
        # mentee
        # favor

        # --- get applications from excel -------------------------------------
        all_applications: Dict[ApplicantType, List[Dict]] = {}
        for applicant_type, fieldpatterns in fieldschemas.items():
            try:
                applications = FuzzyTable(
                    path=self._path,
                    sheetname=applicant_type.name.lower(),
                    fields=fieldpatterns,
                    header_row=1,
                    name=applicant_type.name,
                    missingfieldserror_active=True,
                )
            except fe.MissingFieldError as e:
                msg = str(e) + "/nMake sure your headers are in row 1."
                raise MentormatchError(msg)
            except fe.FuzzyTableError as e:
                raise MentormatchError(str(e))
            all_applications[applicant_type] = [
                dict(record)
                for record in applications.records
            ]

        # --- get "favored" status for mentees --------------------------------
        try:
            favored_mentees = FuzzyTable(
                path=self._path,
                sheetname='favor',
                fields=favor,
                name='favored_mentees',
                approximate_match=False,
                missingfieldserror_active=True,
            )
        except fe.FuzzyTableError as e:
            raise MentormatchError(str(e))
        favored_mentees = {
            mentee['wwid']: mentee['favor']
            for mentee in favored_mentees.records
        }
        for mentee in all_applications[ApplicantType.MENTEE]:
            wwid = mentee['wwid']
            favor_val = favored_mentees.get(wwid, 0)
            mentee['favor'] = favor_val

        # --- return applications ---------------------------------------------
        return all_applications
