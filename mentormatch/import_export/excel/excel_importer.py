from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable
from fuzzytable import exceptions as fe
from mentormatch.db import database
from mentormatch.configuration import fieldschemas, favor
from mentormatch.applicants import Mentors, Mentees
from mentormatch.exceptions import exceptions


class ExcelImporter:

    def __init__(self, path, mentor_dicts, mentee_dicts):
        self.mentor_dicts = mentor_dicts
        self.mentee_dicts = mentee_dicts
        self.path = path

    def get_mentordicts(self):
        pass

    def get_menteedicts(self):
        pass

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
            except FuzzyTableError as e:
                raise exceptions.MentormatchError(str(e))

            # --- add applications to db ------------------------------------------
            records = applications.records  # list of dicts, each representing an applicant
            database.add_group_to_db(group_name=group_name, records=records, database=db)

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
        except FuzzyTableError as e:
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
            'mentors': Mentors(db, self),
            'mentees': Mentees(db, self),
        }

    # def keys(self):
    #     return self._groups.keys()

    # def __getitem__(self, groupname):
    #     return self._groups[groupname]

    def items(self):
        return self._groups.items()

    def __getattr__(self, item):
        return self._groups[item]


if __name__ == '__main__':
    # try:
    #     raise fte.InvalidFileError(None)
    # except fte.FuzzyTableError as e:
    #     msg = str(e)
    #     raise exceptions.MentormatchError(msg)
    pass