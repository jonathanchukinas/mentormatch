from __future__ import annotations
from mentormatch.api.compatibility_checker import Compatibility
from mentormatch.api.utils.enums import YesNoMaybe
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.api.utils.enums import ApplicantType
    from mentormatch.api.pair.pair import Pair


class CompatibilityYearsDelta(Compatibility):
    # Mentor must have at least X more years of experience than mentee.

    def __init__(self, min_years_delta: int):
        self._min_delta = min_years_delta

    def is_compatible(self, pair: Pair) -> bool:
        mentor_years = pair.mentor.years
        mentee_years = pair.mentee.years
        return mentor_years >= (mentee_years + self._min_delta)


class CompatibilityNoPreference(Compatibility):
    # Mentor/ees have the option of saying 'no' to certain genders and
    # locations. This class checks to make sure the 'subject' doesn't get
    # matched to someone with characteristics she's said 'no' to.

    def __init__(self, subject: ApplicantType):
        self._subject = subject

    def is_compatible(self, pair: Pair) -> bool:
        subject = pair.get_applicant(self._subject)
        subject_unwanted_loc_and_gender = subject.get_preference(YesNoMaybe.NO)
        target = pair.get_applicant(self._subject, return_other=True)
        target_loc_and_gender = target.location_and_gender
        return len(subject_unwanted_loc_and_gender & target_loc_and_gender) == 0


class CompatibilityNotSamePerson(Compatibility):
    # Sometimes a person applies to be both mentor and mentee.
    # This makes sure they never get paired with themselves.
    def is_compatible(self, pair: Pair) -> bool:
        return pair.mentor.wwid != pair.mentee.wwid


class CompatibilityLevelDelta(Compatibility):
    # Mentor must be at least one level above mentee (e.g. 4 vs. 3). The one
    # exception to this is that a level 2 is allowed to be paired with another
    # level 2.

    def is_compatible(self, pair: Pair) -> bool:
        mentor_level = pair.mentor.position_level
        mentee_level = pair.mentee.position_level
        return (mentor_level > mentee_level) or (mentor_level == 2 and mentee_level == 2)
