"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants import Mentor


class GroupApplicants:

    def __init__(self, db, all_applicants, applicant_class):
        self.all_applicants = all_applicants
        db_table = db.table(applicant_class.group)
        self._group_applicants = {
            record['wwid']: applicant_class(
                db_table=db_table,
                doc_id=record.doc_id,
                all_applicants=all_applicants,
            )
            for record in db_table.all()
        }

    def __len__(self):
        return len(self._group_applicants)

    # def __getitem__(self, item):
    #     # Return one mentor/ee given her wwid
    #     return self._group_applicants[item]

    def __iter__(self):
        yield from self._group_applicants.values()

    def wwid_get(self, wwid):
        return self._group_applicants[wwid]

    # def keys(self):
    #     """Like ``dict.keys()``.
    #     Return a generator yielding mentor/ee wwids."""
    #     return (key for key in self)
    #
    # def values(self):
    #     """Like ``dict.values()``.
    #     Return a generator yielding mentor/ee objects."""
    #     return (self[key] for key in self.keys())
    #
    # def items(self):
    #     """Like ``dict.items()``.
    #     Return a generator yielding field name / column data tuples."""
    #     return zip(self.keys(), self.values())
