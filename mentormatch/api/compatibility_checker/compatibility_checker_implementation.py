from mentormatch.api.utils.enums import ApplicantType
from mentormatch.api.compatibility_checker import CompatibilityChecker
from mentormatch.api.pair.pair import Pair


class CompatibilityCheckerYearsDelta(CompatibilityChecker):
    # Mentor must have at least X more years of experience than mentee.

    def __init__(self, min_years_delta: int):
        self._min_delta = min_years_delta

    def is_compatible(self, pair: Pair) -> bool:
        mentor_years = pair.mentor.years_experience
        mentee_years = pair.mentee.years_experience
        return mentor_years >= (mentee_years + self._min_delta)


class CompatibilityCheckerNoPreference(CompatibilityChecker):
    # Mentor/ees have the option of saying 'no' to certain genders and
    # locations. This class checks to make sure the 'subject' doesn't get
    # matched to someone with characteristics she's said 'no' to.

    def __init__(self, subject: ApplicantType):
        self._subject = subject

    def is_compatible(self, pair: Pair) -> bool:
        subject = pair.get_applicant(self._subject)
        target = pair.get_applicant(self._subject, return_other=True)
        return len(subject.preference_no & target.location_and_gender) == 0


class CompatibilityCheckerNotSamePerson(CompatibilityChecker):
    # Sometimes a person applies to be both mentor and mentee.
    # This makes sure they never get paired with themselves.
    def is_compatible(self, pair: Pair) -> bool:
        return pair.mentor.wwid != pair.mentee.wwid


class CompatibilityCheckerLevelDelta(CompatibilityChecker):
    # Mentor must be at least one level above mentee (e.g. 4 vs. 3). The one
    # exception to this is that a level 2 is allowed to be paired with another
    # level 2.

    def is_compatible(self, pair: Pair) -> bool:
        mentor_level = pair.mentor.position_level
        mentee_level = pair.mentee.position_level
        if mentor_level > mentee_level:
            return True
        elif mentor_level == 2 and mentee_level == 2:
            return True
        else:
            return False
