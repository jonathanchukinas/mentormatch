from mentormatch.api.applicant.applicant_abc import Applicant
from mentormatch.api.pair.pair import Pair
from mentormatch.api.sorter.sorter_abc import Sorter
from mentormatch.api.sorter.util import (BetterPair, PairAndValue, calc_better_pair)
from mentormatch.utils import MinMax, YesNoMaybe, ApplicantType


class SorterPositionLevel(Sorter):
    # The mentee closer to the mentor's level wins

    def __init__(self, minimize_or_maximize: MinMax):
        self.min_max_mode = minimize_or_maximize

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            pair1=PairAndValue(pair1, pair1.level_delta),
            pair2=PairAndValue(pair2, pair1.level_delta),
            mode=self.min_max_mode,
        )


class SorterLocationAndGender(Sorter):

    def __init__(
        self,
        subject_applicant_type: ApplicantType,
        preference_level: YesNoMaybe,
    ):
        self._subject_applicant_type = subject_applicant_type
        self._preference_level = preference_level

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            pair1=PairAndValue(pair1, self._count_matches(pair1)),
            pair2=PairAndValue(pair2, self._count_matches(pair2)),
            mode=MinMax.MAX,
        )

    def _count_matches(self, pair: Pair) -> int:
        subject = pair.get_applicant(self._subject_applicant_type)
        subject_preferences = subject.get_preference(self._preference_level)
        target = pair.get_applicant(self._subject_applicant_type, return_other=True)
        target_loc_and_gender = target.location_and_gender
        return len(subject_preferences & target_loc_and_gender)


class SorterHash(Sorter):
    # This is an arbitrary tie-breaker.
    # It deterministically 'randomly' selects a winner.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, hash(pair1)),
            PairAndValue(pair2, hash(pair2)),
            mode=MinMax.MAX,
        )


class SorterYearsExperience(Sorter):
    # The mentee closer to the mentor's level wins
    def __init__(self, minimize_or_maximize: MinMax):
        self._min_max_mode = minimize_or_maximize

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, pair1.years_delta),
            PairAndValue(pair2, pair2.years_delta),
            mode=self._min_max_mode,
        )


class SorterPreferredMentorOrder(Sorter):
    # Whichever mentee ranked this mentor higher wins.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._preferredmentor_rankorder(pair1)),
            PairAndValue(pair2, self._preferredmentor_rankorder(pair2)),
            mode=MinMax.MIN,
        )

    @staticmethod
    def _preferredmentor_rankorder(pair: Pair) -> int:
        mentor_wwid = pair.mentor.wwid
        mentee_preferred_wwids = pair.mentee.preferred_wwids
        rankorder = mentee_preferred_wwids.index(mentor_wwid)
        return rankorder


class SorterPreferredMentorCount(Sorter):
    # The mentee who selected more preferred mentors wins.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._wwid_count(pair1)),
            PairAndValue(pair2, self._wwid_count(pair2)),
            mode=MinMax.MAX,
        )

    @staticmethod
    def _wwid_count(pair: Pair) -> int:
        mentee = pair.mentee
        return len(mentee.preferred_wwids)


class SorterFavored(Sorter):
    # The mentee who is more favored (b/c e.g. has been more often or more
    # recently rejected) wins. **This will move up in importance as the mentee
    # fails to pair with one of her preferred mentors.**
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._mentee_favor(pair1)),
            PairAndValue(pair2, self._mentee_favor(pair2)),
            mode=MinMax.MAX,
        )

    @staticmethod
    def _mentee_favor(pair: Pair) -> int:
        favor = pair.mentee.favor
        return favor


class SorterPrefVsRand(Sorter):
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, pair1.pair_type),
            PairAndValue(pair2, pair2.pair_type),
            mode=MinMax.MAX,
        )


class SorterSkillsAndFunctions(Sorter):
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._get_numerical_rating(pair1)),
            PairAndValue(pair2, self._get_numerical_rating(pair2)),
            mode=MinMax.MAX,
        )

    def _get_numerical_rating(self, pair: Pair) -> float:
        function_match = self._function_match(pair.mentor, pair.mentee)
        skills_match = self._skills_match(pair.mentor, pair.mentee)
        return function_match + skills_match

    @staticmethod
    def _function_match(mentor: Applicant, mentee: Applicant) -> int:
        return len(mentor.function & mentee.function)

    @staticmethod
    def _skills_match(mentor: Applicant, mentee: Applicant) -> float:
        count_mentee_skills = len(mentee.skills)
        if count_mentee_skills == 0:
            return 0
        return len(mentor.skills & mentee.skills) / count_mentee_skills
