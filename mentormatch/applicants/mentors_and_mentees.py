"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants import Mentor, Mentee


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


class Mentors(GroupApplicants):

    def __init__(self, db, all_applicants):
        super().__init__(db, all_applicants, Mentor)

    def __getitem__(self, wwid) -> Mentor:
        return self._group_applicants.get(wwid, None)


class Mentees(GroupApplicants):

    def __init__(self, db, all_applicants):
        super().__init__(db, all_applicants, Mentee)
        self.queue = None  # add right, pop left

    def awaiting_preferred_mentor(self):
        if self.queue is None:
            randomly_sorted_mentees = sorted(self._group_applicants.items(), key=lambda mentee: mentee.hash)
            self.queue = collections.deque(randomly_sorted_mentees)
        try:
            yield self.queue.popleft()
        except IndexError:
            self.queue = None
            return


if __name__ == '__main__':
    pass
