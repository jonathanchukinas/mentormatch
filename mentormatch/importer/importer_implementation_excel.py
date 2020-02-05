from __future__ import annotations
from fuzzytable import FuzzyTable, exceptions as fe
from .importer_implementation_excel_schema import fieldschemas, favor
from .importer_abc import Importer
from mentormatch.utils.exceptions import MentormatchError
import mentormatch.utils as utils
from typing import Dict, List, TYPE_CHECKING


class ImporterExcel(Importer):

    def __init__(self, path):
        self._path = path

    def execute(self) -> Dict[utils.ApplicantType, List[Dict]]:

        # For this to work, there needs to be one excel workbook with the following worksheets:
        # mentor
        # mentee
        # favor

        # --- get applications from excel -------------------------------------
        all_applications: Dict[utils.ApplicantType, List[Dict]] = {}
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
            except fe.MissingFieldError as e:  # pragma: no cover
                msg = str(e) + "/nMake sure your headers are in row 1."
                raise MentormatchError(msg)
            except fe.FuzzyTableError as e:  # pragma: no cover
                raise MentormatchError(str(e))
            application_list = []
            locs_and_genders = utils.ApplicationSchema.get_locations_and_genders()
            for record in applications.records:
                application = dict(record)
                application.update({
                    val.get_preference_key(): []
                    for val in utils.YesNoMaybe
                })
                for loc_or_gender in locs_and_genders:  # e.g. 'horsham'
                    pref_str = application.pop(loc_or_gender)  # e.g. 'no'
                    pref_key = utils.YesNoMaybe.get_enum(pref_str).get_preference_key()  # e.g. 'preference_no'
                    application[pref_key] = loc_or_gender
                application_list.append(application)
            all_applications[applicant_type] = application_list

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
        except fe.FuzzyTableError as e:  # pragma: no cover
            raise MentormatchError(str(e))
        favored_mentees = {
            mentee['wwid']: mentee['favor']
            for mentee in favored_mentees.records
        }
        for mentee in all_applications[utils.ApplicantType.MENTEE]:
            wwid = mentee['wwid']
            favor_val = favored_mentees.get(wwid, 0)
            mentee['favor'] = favor_val

        # --- return applications ---------------------------------------------
        return all_applications
