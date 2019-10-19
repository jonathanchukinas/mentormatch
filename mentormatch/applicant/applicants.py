"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants.applicant import Applicant


class Applicants(collections.abc.Sequence):

    def __init__(self, worksheet):
        """Objects of this class will house either all mentors or all mentees"""
        self.ws = worksheet
        applicant_count = len(worksheet.df)
        self._applicants = [Applicant(worksheet, index) for index in range(applicant_count)]

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


if __name__ == '__main__':
    pass
