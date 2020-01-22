from mentormatch.applicants.applicant_base import ApplicantType
from mentormatch.pair_compatibility.pair_compatibility_abstract import PairChecker
from mentormatch.pair.pair_base import Pair


class PairCompatibilityYearsDelta(PairChecker):
    # Mentor must have at least X more years of experience than mentee.

    def __init__(self, min_years_delta: int):
        self._min_delta = min_years_delta

    def is_compatible(self, pair: Pair) -> bool:
        mentor_years = pair.mentor.years_experience
        mentee_years = pair.mentee.years_experience
        return mentor_years >= (mentee_years + self._min_delta)


class PairCompatibilityNoPreference(PairChecker):
    # Mentor/ees have the option of saying 'no' to certain genders and locations.
    # This checks to make sure the 'subject' doesn't get matched to someone with
    # characteristics she's said 'no' to.

    def __init__(self, subject: ApplicantType):
        self._subject = subject

    def is_compatible(self, pair: Pair) -> bool:
        subject = pair.get_applicant(self._subject)
        target = pair.get_applicant(self._subject, return_other=True)
        return len(subject.preference_no & target.location_and_gender) == 0


class PairCompatibilityNotSamePerson(PairChecker):
    # Sometimes a person applies to be both mentor and mentee.
    # This makes sure they never get paired with themselves.
    def is_compatible(self, pair: Pair) -> bool:
        return pair.mentor.wwid != pair.mentee.wwid


class PairCompatibilityLevelDelta(PairChecker):
    # Mentor must be at least one level above mentee (e.g. 4 vs. 3).
    # The one exception to this is that a level 2 is allowed to be paired with another level 2.

    def is_compatible(self, pair: Pair) -> bool:
        mentor_level = pair.mentor.position_level
        mentee_level = pair.mentee.position_level
        if mentor_level > mentee_level:
            return True
        elif mentor_level == 2 and mentee_level == 2:
            return True
        else:
            return False
