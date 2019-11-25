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
        self._applicants = [
            applicant_constructor(record.doc_id)
            for record in table.all()
        ]

    def __getitem__(self, wwid):
        # TODO 20191125 this needs updated
        df = self.ws.df
        indices = df.loc[df[column] == value].index.values
        if len(indices) > 0:
            index = indices[0]
            return self[index]
        else:
            return None


class Mentors(GroupApplicants):

    def __init__(self, db, all_applicants):
        super().__init__(db, all_applicants, Mentor)


class Mentees(GroupApplicants):

    def __init__(self, db, all_applicants):
        super().__init__(db, all_applicants, Mentee)
        self._queue = None

    def awaiting_preferred_mentor(self):
        if self._queue is None:
            self._queue = collections.deque(self._applicants)
        try:
            yield self._queue.popleft()
        except IndexError:
            self._queue = None
            return


if __name__ == '__main__':
    pass
