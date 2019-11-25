"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicant.applicant import Mentor, Mentee


class Applicants(collections.abc.Sequence):

    def __len__(self):
        return len(self.ws)

    def __getitem__(self, item):
        return self._applicants[item]

    def get_applicant(self, column, value):
        df = self.ws.df
        indices = df.loc[df[column] == value].index.values
        if len(indices) > 0:
            index = indices[0]
            return self[index]
        else:
            return None


class Mentors(Applicants):
    pass


class Mentees(Applicants):

    def __init__(self, db):
        table = db.table('mentees')
        self._mentees = [
            Mentee(record.doc_id)
            for record in table.all()
        ]


        

    def awaiting_preferred_mentor(self):
        yield "the next mentee in line"



if __name__ == '__main__':
    pass
