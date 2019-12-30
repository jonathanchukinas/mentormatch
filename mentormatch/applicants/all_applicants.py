# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
from fuzzytable.exceptions import FuzzyTableError
from fuzzytable import FuzzyTable
from fuzzytable import exceptions as fe
import toml

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.db import database
from mentormatch.schema import fieldschemas, favor
from mentormatch.applicants import Mentors, Mentees
from mentormatch.main import exceptions


class AllApplicants:

    def __init__(self, path):

        self.excel_path = path

        # --- initialize db ---------------------------------------------------
        db = database.get_clean_db()

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

    def write_to_toml(self):

        # First two dictionaries: mentors and mentees
        results_dict = {}  # keys: mentors/ees
        for groupname, applicants in self.items():
            group_dict = {
                str(applicant): dict(applicant)
                for applicant in applicants
            }
            results_dict[groupname] = group_dict

        # Third dictionary: pairs as wwids
        # key: mentor wwid
        # value: list of mentee wwids
        pairs = {}
        results_dict['pairs'] = pairs
        for mentor in self.mentors:
            mentor_wwid = str(mentor.wwid)
            mentor_pairedmenteewwids = [
                pair.mentee.wwid
                for pair in mentor.assigned_pairs
            ]
            pairs[mentor_wwid] = mentor_pairedmenteewwids

        # Write dicts to toml
        applicants_tomlstring = toml.dumps(results_dict)
        toml_path = self.excel_path.parent / "matching_results.toml"
        toml_path.touch()
        with open(toml_path, "w") as f:
            f.write(applicants_tomlstring)


if __name__ == '__main__':
    # try:
    #     raise fte.InvalidFileError(None)
    # except fte.FuzzyTableError as e:
    #     msg = str(e)
    #     raise exceptions.MentormatchError(msg)
    pass
