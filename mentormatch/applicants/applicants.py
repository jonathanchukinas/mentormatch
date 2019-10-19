"""The Applicant object represents a single applicant. It stores very little
data on its own. It has access to a Worksheet object"""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants.applicant import Applicant


class Applicants:

    def __init__(self, worksheet):
        """Objects of this class will house either all mentors or all mentees"""
        self.ws = worksheet
        applicant_count = len(worksheet.df)
        self._applicants = [Applicant(worksheet, index) for index in range(applicant_count)]

    def generate_unique_applicants(self):
        applicants = [self.__generate_applicant(row_) for row_ in self.__worksheet]
        unique_wwids = set([applicant.data.wwid for applicant in applicants])
        unique_applicants = []
        for wwid in unique_wwids:
            applicants_with_this_wwid = [applicant for applicant in applicants if applicant.data.wwid == wwid]
            most_recent_of_these_applicants = self.__get_most_recent_applicant(applicants_with_this_wwid)
            unique_applicants.append(most_recent_of_these_applicants)
        return unique_applicants

    def __generate_applicant(self, row_):
        available_classes = {'mentors': MentorApplicant,
                             'mentees': MenteeApplicant}
        applicant_class = available_classes[self.__applicant_group]
        applicant = applicant_class(row_)
        return applicant

    def get_applicant_by_wwid(self, wwid):
        wrapped_applicant: ApplicantWrapper
        for wrapped_applicant in self.__wrapped_applicants:
            if wwid == wrapped_applicant.data.
                return wrapped_applicant
        logging.debug(f'No applicant found who has WWID: {wwid}')
        return None
        # TODO Back in Applications, need to validate the WWIDs.
        #  Make sure each mentee's preferred wwwids match a mentor.

    # BOTH
    def contains_applicant(self, wwid):
        found_applicant = False
        if self.get_applicant_by_wwid(wwid) is not None:
            found_applicant = True
        return found_applicant


if __name__ == '__main__':
    pass
