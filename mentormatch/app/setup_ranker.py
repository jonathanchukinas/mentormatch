import mentormatch.ranker as pr
from mentormatch.utils.enums import ApplicantType, YesNoMaybe, MinMax, PairType


_pr_pref_vs_rand = pr.RankerPrefVsRand()
_pr_mentor_yesnomaybe = pr.RankerLocationAndGender(
    ApplicantType.MENTOR, YesNoMaybe.YES)
_pr_mentee_yesnomaybe = pr.RankerLocationAndGender(
    ApplicantType.MENTEE, YesNoMaybe.YES)
_pr_level_delta_maximize = pr.RankerPositionLevel(
    minimize_or_maximize=MinMax.MAX)
_pr_level_delta_minimize = pr.RankerPositionLevel(
    minimize_or_maximize=MinMax.MIN)
_pr_years_delta_maximize = pr.RankerYearsExperience(
    minimize_or_maximize=MinMax.MAX)
_pr_years_delta_minimize = pr.RankerYearsExperience(
    minimize_or_maximize=MinMax.MIN)
_pr_preferred_mentor_count = pr.RankerPreferredMentorCount()
_pr_preferred_mentor_order = pr.RankerPreferredMentorOrder()
_pr_skills_and_functions = pr.RankerSkillsAndFunctions()
_pr_favored = pr.RankerFavored()
_pr_hash = pr.RankerHash()


###################
# CONTEXT MANAGER #
###################
pair_ranker_context_manager = pr.RankerContextMgr()


#################################
# PREFERRED RANKING, MENTEE POV #
#################################
_ranker_preferred_mentee_initialization = _pr_preferred_mentor_count
pair_ranker_context_manager.register(
    key=(PairType.PREFERRED, ApplicantType.MENTEE),
    pair_ranker=_ranker_preferred_mentee_initialization,
)


#################################
# PREFERRED RANKING, MENTOR POV #
#################################
_ranker_preferred = pr.RankerAggregatorFavor(
    pair_rankers=[
        _pr_pref_vs_rand,
        _pr_mentor_yesnomaybe,
        _pr_level_delta_minimize,
        _pr_years_delta_minimize,
        _pr_preferred_mentor_order,
        _pr_preferred_mentor_count,
        _pr_hash,
    ],
    pair_ranker_favor=_pr_favored,
    pair_ranker_favor_min_position=1,
)
pair_ranker_context_manager.register(
    key=(PairType.PREFERRED, ApplicantType.MENTOR),
    pair_ranker=_ranker_preferred,
)


##############################
# RANDOM RANKING, MENTEE POV #
##############################
_WPR = pr.WeightedPairRanker
_ranker_random_mentee_initialization = pr.RankerAggregatorWeighted(
    weighted_pair_rankers=[
        _WPR(_pr_mentee_yesnomaybe, 1),
        _WPR(_pr_skills_and_functions, 1),
        _WPR(_pr_level_delta_maximize, 1),
        _WPR(_pr_years_delta_maximize, 1),
        _WPR(_pr_hash, 0.1),            # TODO get pair's hash
    ],
)
pair_ranker_context_manager.register(
    key=(PairType.RANDOM, ApplicantType.MENTEE),
    pair_ranker=_ranker_random_mentee_initialization,
)


##############################
# RANDOM RANKING, MENTOR POV #
##############################
_ranker_random = pr.RankerAggregatorFavor(
    pair_rankers=[
        _pr_pref_vs_rand,
        _pr_mentor_yesnomaybe,
        _pr_mentee_yesnomaybe,
        _pr_level_delta_minimize,
        _pr_years_delta_minimize,
        _pr_skills_and_functions,
        _pr_hash,
    ],
    pair_ranker_favor=_pr_favored,
    pair_ranker_favor_min_position=1,
)
pair_ranker_context_manager.register(
    key=(PairType.RANDOM, ApplicantType.MENTOR),
    pair_ranker=_ranker_random,
)
