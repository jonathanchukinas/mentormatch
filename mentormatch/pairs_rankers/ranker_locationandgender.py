from mentormatch.pairs_rankers.ranker_abstract import IPairRanker, BetterPair, YesNoMaybe, \
    ApplicantType, PairAndValue, _calc_better_pair
from mentormatch.pairs.pair_base import BasePair
from mentormatch.applicants.applicant_base import ApplicantBase


class RankerLocationAndGender(IPairRanker):

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

    def _get_single_pair_overlap(self, pair: BasePair):
        agent_preferences = getattr(self._get_agent(pair), self._pref_level_attribute)
        target_characteristic = self._get_agent(pair).location_and_gender
        return agent_preferences & target_characteristic

    def _get_agent(self, pair: BasePair) -> ApplicantBase:
        if self._agent == 'mentor':
            return pair.mentor
        elif self._agent == 'mentee':
            return pair.mentee
        else:
            raise ValueError

    def _get_target(self, pair: BasePair) -> ApplicantBase:
        if self._agent == 'mentor':
            return pair.mentee
        elif self._agent == 'mentee':
            return pair.mentor
        else:
            raise ValueError

    def get_better_pair(self, pair1: BasePair, pair2: BasePair) -> BetterPair:

        return _calc_better_pair(
            pair1=PairAndValue(pair1, self._get_single_pair_overlap(pair1)),
            pair2=PairAndValue(pair2, self._get_single_pair_overlap(pair2)),
        )


