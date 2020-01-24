from mentormatch.applicants.applicant_base import (
    ApplicantType, ApplicantBase, Mentee, Mentor)
from mentormatch.pair.pair_base import Pair
from mentormatch.pair_ranker.pair_ranker_abstract import PairRanker
from mentormatch.pair_ranker.util import PairsEqual, BetterPair, YesNoMaybe, PairAndValue, calc_better_pair, calc_better_pair_list


class RankerPositionLevel(PairRanker):
    # The mentee closer to the mentor's level wins
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        if pair1.position_delta == pair2.pos:
            return PairsEqual
        elif pair1.position_delta > pair2.position_delta:
            return pair1
        else:
            return pair2

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:

        return calc_better_pair(
            pair1=PairAndValue(pair1, hash(pair1)),
            pair2=PairAndValue(pair2, hash(pair2)),
        )


class RankerLocationAndGender(PairRanker):

    def __init__(self, agent: ApplicantType, preference_level: YesNoMaybe):

        # Validate agent
        applicant_types = 'mentor mentee'.split()
        if agent in applicant_types:
            self._agent = agent
        else:
            raise ValueError(f"agent must be in {applicant_types}")

        # Validate preference_level
        yesnomaybe = 'yes no maybe'.split()
        if preference_level in yesnomaybe:
            self._pref_level_attribute = f"preference_{preference_level}"
        else:
            raise ValueError(f"preference_level must be in {yesnomaybe}")

    def _get_single_pair_overlap(self, pair: Pair):
        agent_preferences = getattr(self._get_agent(pair), self._pref_level_attribute)
        target_characteristic = self._get_agent(pair).location_and_gender
        return agent_preferences & target_characteristic

    def _get_agent(self, pair: Pair) -> ApplicantBase:
        if self._agent == 'mentor':
            return pair.mentor
        elif self._agent == 'mentee':
            return pair.mentee
        else:
            raise ValueError

    def _get_target(self, pair: Pair) -> ApplicantBase:
        if self._agent == 'mentor':
            return pair.mentee
        elif self._agent == 'mentee':
            return pair.mentor
        else:
            raise ValueError

    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:

        return self._calc_better_pair(
            pair1=PairAndValue(pair1, self._get_single_pair_overlap(pair1)),
            pair2=PairAndValue(pair2, self._get_single_pair_overlap(pair2)),
        )


class PairRankerHash(PairRanker):
    # This is an arbitrary tie-breaker.
    # It deterministically 'randomly' selects a winner.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, hash(pair1)),
            PairAndValue(pair2, hash(pair2)),
            mode='max',
        )


class RankerYearsExperience(PairRanker):
    # The mentee closer to the mentor's level wins
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, pair1.years_delta),
            PairAndValue(pair2, pair2.years_delta),
            mode='max',
        )


class PairRankerPreferredMentorOrder(PairRanker):
    # Whichever mentee ranked this mentor higher wins.
    def get_better_pair(self, pair1: Pair, pair2: Pair) -> BetterPair:
        return calc_better_pair(
            PairAndValue(pair1, self._preferredmentor_rankorder(pair1)),
            PairAndValue(pair2, self._preferredmentor_rankorder(pair2)),
            mode='min',
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
            mode='max',
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
            mode='max',
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
            mode='max',
        )

    def _get_numerical_rating(self, pair: Pair) -> float:
        function_match = self._function_match(pair.mentor, pair.mentee)
        skills_match = self._skills_match(pair.mentor, pair.mentee)
        return function_match + skills_match
        # TODO Go back to setting up the pair rankers in config

    @staticmethod
    def _function_match(mentor: ApplicantBase, mentee: ApplicantBase) -> int:
        return len(mentor.functions & mentee.functions)

    @staticmethod
    def _skills_match(mentor: ApplicantBase, mentee: ApplicantBase) -> float:
        return len(mentor.skills & mentee.skills) / len(mentee.skills)
