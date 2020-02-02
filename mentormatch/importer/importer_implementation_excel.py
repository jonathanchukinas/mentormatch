from __future__ import annotations
from fuzzytable import FuzzyTable, exceptions as fe
from .importer_implementation_excel_schema import fieldschemas, favor
from .importer_abc import Importer
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType
    from mentormatch.api.applicant import Mentor


# TODO delete:
"""
Steps:
Get path via tkinter
Pass path to Excel Importer, returns dicts
Save to toml file?
Read from toml file
Return dicts
"""


class ImporterExcel(Importer):

    def __init__(self, path):
        self._path = path

    def execute(self) -> Dict[ApplicantType, List[Dict]]:
        raise NotImplementedError

    def _get_applicant_dicts(self):

        # --- get applications from excel -------------------------------------
        for group_name, fieldpatterns in fieldschemas.items():
            try:
                applications = FuzzyTable(
                    path=path,
                    sheetname=group_name,
                    fields=fieldpatterns,
                    header_row=1,
                    name=group_name,
                    missingfieldserror_active=True,
                )
            except fe.MissingFieldError as e:
                msg = str(e) + "/nMake sure your headers are in row 1."
                raise exceptions.MentormatchError(msg)
            except fe.FuzzyTableError as e:
                raise exceptions.MentormatchError(str(e))



        # --- get "favored" status for mentees --------------------------------
        try:
            favored_mentees = FuzzyTable(
                path=path,
                sheetname='favor',
                fields=favor,
                name='favored_mentees',
                approximate_match=False,
                missingfieldserror_active=True,
            )
        except fe.FuzzyTableError as e:
            raise exceptions.MentormatchError(str(e))
        favored_mentees = {
            mentee['wwid']: mentee['favor']
            for mentee in favored_mentees.records
        }
        mentee_table = db.table('mentees')
        mentees = mentee_table.all()
        for mentee in mentees:
            wwid = mentee['wwid']
            favor_val = favored_mentees.get(wwid, 0)
            mentee['favor'] = favor_val
        mentee_table.write_back(mentees)

        # --- create applicants -----------------------------------------------
        self._groups = {
            'mentors': Mentor(db, self),
            'mentees': Mentees(db, self),
        }

    def items(self):
        return self._groups.items()

    def __getattr__(self, item):
        return self._groups[item]
