import mentormatch.api.sorter.sorter_implementation as si
import mentormatch.api.sorter.sorter_aggregator as sa
import mentormatch.api.sorter.sorter_context_mgr as scm
import mentormatch.api.sorter.util as su
from mentormatch.api.utils.enums import ApplicantType, YesNoMaybe, MinMax, PairType


########################
# Sorter Implentations #
########################
_pr_pref_vs_rand = si.SorterPrefVsRand()
_pr_mentor_yesnomaybe = si.SorterLocationAndGender(
    ApplicantType.MENTOR, YesNoMaybe.YES)
_pr_mentee_yesnomaybe = si.SorterLocationAndGender(
    ApplicantType.MENTEE, YesNoMaybe.YES)
_pr_level_delta_maximize = si.SorterPositionLevel(
    minimize_or_maximize=MinMax.MAX)
_pr_level_delta_minimize = si.SorterPositionLevel(
    minimize_or_maximize=MinMax.MIN)
_pr_years_delta_maximize = si.SorterYearsExperience(
    minimize_or_maximize=MinMax.MAX)
_pr_years_delta_minimize = si.SorterYearsExperience(
    minimize_or_maximize=MinMax.MIN)
_pr_preferred_mentor_count = si.SorterPreferredMentorCount()
_pr_preferred_mentor_order = si.SorterPreferredMentorOrder()
_pr_skills_and_functions = si.SorterSkillsAndFunctions()
_pr_favored = si.SorterFavored()
_pr_hash = si.SorterHash()


#################################
# PREFERRED RANKING, MENTEE POV #
#################################
_ranker_preferred_mentee_initialization = _pr_preferred_mentor_count


#################################
# PREFERRED RANKING, MENTOR POV #
#################################
_ranker_preferred = sa.SorterAggregatorFavor(
    sorters=[
        _pr_pref_vs_rand,
        _pr_mentor_yesnomaybe,
        _pr_level_delta_minimize,
        _pr_years_delta_minimize,
        _pr_preferred_mentor_order,
        _pr_preferred_mentor_count,
        _pr_hash,
    ],
    sorter_favor=_pr_favored,
    sorter_favor_min_position=1,
)


##############################
# RANDOM RANKING, MENTEE POV #
##############################
_WPR = su.WeightedSorter
_ranker_random_mentee_initialization = sa.SorterAggregatorWeighted(
    weighted_sorters=[
        _WPR(_pr_mentee_yesnomaybe, 1),
        _WPR(_pr_skills_and_functions, 1),
        _WPR(_pr_level_delta_maximize, 1),
        _WPR(_pr_years_delta_maximize, 1),
        _WPR(_pr_hash, 0.1)
    ],
)


##############################
# RANDOM RANKING, MENTOR POV #
##############################
_ranker_random = sa.SorterAggregatorFavor(
    sorters=[
        _pr_pref_vs_rand,
        _pr_mentor_yesnomaybe,
        _pr_mentee_yesnomaybe,
        _pr_level_delta_minimize,
        _pr_years_delta_minimize,
        _pr_skills_and_functions,
        _pr_hash,
    ],
    sorter_favor=_pr_favored,
    sorter_favor_min_position=1,
)


####################
# CONTEXT MANAGERS #
####################
_sorter_context_manager_preferred = scm.SorterContextMgr(
    initial_sorter=_ranker_preferred_mentee_initialization,
    match_sorter=_ranker_preferred,
)
_sorter_context_manager_random = scm.SorterContextMgr(
    initial_sorter=_ranker_random_mentee_initialization,
    match_sorter=_ranker_random,
)
_sorters = {
    PairType.PREFERRED: _sorter_context_manager_preferred,
    PairType.RANDOM: _sorter_context_manager_random
}
