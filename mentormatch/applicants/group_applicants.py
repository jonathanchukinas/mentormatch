"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants import Mentor, Mentee


class GroupApplicants:

    def __init__(self, db, all_applicants, applicant_constructor):
        self.all_applicants = all_applicants
        table = db.table(applicant_constructor.group)
        self._group_applicants = {
            record.wwid: applicant_constructor(record.doc_id)
            for record in table.all()
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
            self.queue = collections.deque(self._group_applicants.items())
        try:
            yield self.queue.popleft()
        except IndexError:
            self.queue = None
            return


if __name__ == '__main__':
    pass
