# --- Standard Library Imports ------------------------------------------------
from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.db import database
from mentormatch.excel import fieldschema
from mentormatch.excel.fieldschema import fieldschema
from mentormatch.applicants import Mentors, Mentees
from mentormatch.main import exceptions


class AllApplicants:

    def __init__(self, path):

        # --- initialize db -------------------------------------------------------
        db = database.get_clean_db()

        # --- get applications from excel -----------------------------------------
        for group_name, fieldpatterns in fieldschema.items():
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
                # TODO I don't think this is the right way to pass an exception message to another.
                raise exceptions.MentormatchError(e)

        # --- add applications to db ----------------------------------------------
            records = applications.records  # list of dicts, each representing an applicant
            database.add_group_to_db(group_name=group_name, records=records, database=db)

        # --- create applicants -----------------------------------------------
        self.mentors = Mentors(db, self)
        self.mentees = Mentees(db, self)