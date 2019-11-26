# --- Standard Library Imports ------------------------------------------------
from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.db import database
from mentormatch.schema import favored, fieldschemas
from mentormatch.applicants import Mentors, Mentees
from mentormatch.main import exceptions


class AllApplicants:

    def __init__(self, path):

        # --- initialize db ---------------------------------------------------
        db = database.get_clean_db()

        # --- get applications from excel -------------------------------------
        for group_name, fieldpatterns in fieldschemas.items():
            try:
                applications = FuzzyTable(
                    path=path,
                    sheetname=group_name,
                    fields=fieldpatterns,
                    header_row_seek=True,
                    name=group_name,
                    approximate_match=False,
                    missingfieldserror_active=True,
                )
            except FuzzyTableError as e:
                raise exceptions.MentormatchError(str(e))

        # --- add applications to db ------------------------------------------
            records = applications.records  # list of dicts, each representing an applicant
            database.add_group_to_db(group_name=group_name, records=records, database=db)

        # --- get "favored" status for mentees --------------------------------
        try:
            favored_mentees = FuzzyTable(
                path=path,
                sheetname='favored',
                fields=favored,
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
        mentee_table = db['mentees']
        mentees = mentee_table.all()
        for mentee in mentees:
            wwid = mentee['wwid']
            favor = favored_mentees.get(wwid, 0)
            mentee['favor'] = favor
        mentee_table.write_back(mentees)

        # --- create applicants -----------------------------------------------
        self.mentors = Mentors(db, self)
        self.mentees = Mentees(db, self)


if __name__ == '__main__':
    # try:
    #     raise fte.InvalidFileError(None)
    # except fte.FuzzyTableError as e:
    #     msg = str(e)
    #     raise exceptions.MentormatchError(msg)
    pass
