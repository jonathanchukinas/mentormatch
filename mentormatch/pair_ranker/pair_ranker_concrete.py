from mentormatch.applicants.applicant_base import ApplicantBase
from mentormatch.pair.pair_base import Pair
from mentormatch.pair_ranker.pair_ranker_abstract import PairRanker
from mentormatch.pair_ranker.util import (
    calc_better_pair_list, BetterPair, PairAndValue, calc_better_pair)
from mentormatch.utils.enums import MinMax, YesNoMaybe, ApplicantType


class PairRankerPositionLevel(PairRanker):
    # The mentee closer to the mentor's level wins

    def __init__(self, minimize_or_maximize: MinMax):
        self.min_max_mode = minimize_or_maximize

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            pair1=PairAndValue(pair1, pair1.position_delta),
            pair2=PairAndValue(pair2, pair1.position_delta),
            mode=self.min_max_mode,
        )


class PairRankerLocationAndGender(PairRanker):
    # TODO Add comments

    def __init__(
        self,
        agent: ApplicantType,
        preference_level: YesNoMaybe,
    ):
        self._agent = agent
        self._preference_level = preference_level

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            pair1=PairAndValue(pair1, self._count_matches(pair1)),
            pair2=PairAndValue(pair2, self._count_matches(pair2)),
            mode=MinMax.MAX,
        )

    def _count_matches(self, pair: Pair) -> int:
        agent_preferences = pair.get_applicant(self._agent)
        target_characteristic = pair.get_applicant(
            self._agent,
            return_other=True
        )
        return len(agent_preferences & target_characteristic)


class PairRankerHash(PairRanker):
    # This is an arbitrary tie-breaker.
    # It deterministically 'randomly' selects a winner.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, hash(pair1)),
            PairAndValue(pair2, hash(pair2)),
            mode=MinMax.MAX,
        )


class PairRankerYearsExperience(PairRanker):
    # The mentee closer to the mentor's level wins
    def __init__(self, minimize_or_maximize: MinMax):
        self._min_max_mode = minimize_or_maximize

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, pair1.years_delta),
            PairAndValue(pair2, pair2.years_delta),
            mode=self._min_max_mode,
        )


class PairRankerPreferredMentorOrder(PairRanker):
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


class PairRankerPreferredMentorCount(PairRanker):
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


class PairRankerFavored(PairRanker):
    # The mentee who is more favored (b/c e.g. has been more often or more recently rejected) wins.
    # **This will move up in importance as the mentee fails to pair with one of her preferred mentors.**
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._mentee_favor(pair1)),
            PairAndValue(pair2, self._mentee_favor(pair2)),
            mode=MinMax.MAX,
        )

    @staticmethod
    def _mentee_favor(pair: Pair) -> int:
        mentee = pair.mentee
        return len(mentee.favor)


class PairRankerPrefVsRand(PairRanker):
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        pair_types_descending = 'preferred random'.split()  # TODO replace with the new enum
        return calc_better_pair_list(
            PairAndValue(pair1, pair1.pair_type),
            PairAndValue(pair2, pair2.pair_type),
            descending_list=pair_types_descending,
        )


class PairRankerSkillsAndFunctions(PairRanker):
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
    def _function_match(mentor: ApplicantBase, mentee: ApplicantBase) -> int:
        return len(mentor.functions & mentee.functions)

    @staticmethod
    def _skills_match(mentor: ApplicantBase, mentee: ApplicantBase) -> float:
        return len(mentor.skills & mentee.skills) / len(mentee.skills)
