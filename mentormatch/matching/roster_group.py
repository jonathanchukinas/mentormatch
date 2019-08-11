# from bin.__applicants.mentor_mentee import MentorApplicant, MenteeApplicant
import logging
from bin.roster.mentor_mentee import ApplicantWrapper

class RosterGroup:

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

