import mentormatch.ranker as pr
from mentormatch.utils.enums import ApplicantType, YesNoMaybe, MinMax, PairType


########################
# Sorter Implentations #
########################
_pr_pref_vs_rand = pr.SorterPrefVsRand()
_pr_mentor_yesnomaybe = pr.SorterLocationAndGender(
    ApplicantType.MENTOR, YesNoMaybe.YES)
_pr_mentee_yesnomaybe = pr.SorterLocationAndGender(
    ApplicantType.MENTEE, YesNoMaybe.YES)
_pr_level_delta_maximize = pr.SorterPositionLevel(
    minimize_or_maximize=MinMax.MAX)
_pr_level_delta_minimize = pr.SorterPositionLevel(
    minimize_or_maximize=MinMax.MIN)
_pr_years_delta_maximize = pr.SorterYearsExperience(
    minimize_or_maximize=MinMax.MAX)
_pr_years_delta_minimize = pr.SorterYearsExperience(
    minimize_or_maximize=MinMax.MIN)
_pr_preferred_mentor_count = pr.SorterPreferredMentorCount()
_pr_preferred_mentor_order = pr.SorterPreferredMentorOrder()
_pr_skills_and_functions = pr.SorterSkillsAndFunctions()
_pr_favored = pr.SorterFavored()
_pr_hash = pr.SorterHash()


#################################
# PREFERRED RANKING, MENTEE POV #
#################################
_ranker_preferred_mentee_initialization = _pr_preferred_mentor_count


#################################
# PREFERRED RANKING, MENTOR POV #
#################################
_ranker_preferred = pr.SorterAggregatorFavor(
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


##############################
# CONTEXT MANAGER, PREFERRED #
##############################
sorter_context_manager_preferred = pr.SorterContextMgr(
    initial_sorter=_ranker_preferred_mentee_initialization,
    match_sorter=_ranker_preferred,
)


##############################
# RANDOM RANKING, MENTEE POV #
##############################
_WPR = pr.WeightedPairRanker
_ranker_random_mentee_initialization = pr.SorterAggregatorWeighted(
    weighted_pair_rankers=[
        _WPR(_pr_mentee_yesnomaybe, 1),
        _WPR(_pr_skills_and_functions, 1),
        _WPR(_pr_level_delta_maximize, 1),
        _WPR(_pr_years_delta_maximize, 1),
        _WPR(_pr_hash, 0.1),            # TODO get pair's hash
    ],
)


##############################
# RANDOM RANKING, MENTOR POV #
##############################
_ranker_random = pr.SorterAggregatorFavor(
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


###########################
# CONTEXT MANAGER, RANDOM #
###########################
sorter_context_manager_random = pr.SorterContextMgr(
    initial_sorter=_ranker_random_mentee_initialization,
    match_sorter=_ranker_random,
)
