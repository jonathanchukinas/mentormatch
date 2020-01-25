import mentormatch.pair_ranker as pr
from mentormatch.utils.enums import ApplicantType, YesNoMaybe, MinMax, PairType


pr_pref_vs_rand = pr.PairRankerPrefVsRand()
pr_mentor_yesnomaybe = pr.PairRankerLocationAndGender(
    ApplicantType.MENTOR, YesNoMaybe.YES)
pr_mentee_yesnomaybe = pr.PairRankerLocationAndGender(
    ApplicantType.MENTEE, YesNoMaybe.YES)
pr_level_delta_maximize = pr.PairRankerPositionLevel(
    minimize_or_maximize=MinMax.MAX)
pr_level_delta_minimize = pr.PairRankerPositionLevel(
    minimize_or_maximize=MinMax.MIN)
pr_years_delta_maximize = pr.PairRankerYearsExperience(
    minimize_or_maximize=MinMax.MAX)
pr_years_delta_minimize = pr.PairRankerYearsExperience(
    minimize_or_maximize=MinMax.MIN)
pr_preferred_mentor_count = pr.PairRankerPreferredMentorCount()
pr_preferred_mentor_order = pr.PairRankerPreferredMentorOrder()
pr_skills_and_functions = pr.PairRankerSkillsAndFunctions()
pr_favored = pr.PairRankerFavored()
pr_hash = pr.PairRankerHash()


###################
# CONTEXT MANAGER #
###################
pair_ranker_context_manager = pr.PairRankerContextMgr()


#################################
# PREFERRED RANKING, MENTEE POV #
#################################
ranker_preferred_mentee_initialization = pr_preferred_mentor_count
pair_ranker_context_manager.register(
    key=(PairType.PREFERRED, ApplicantType.MENTEE),
    pair_ranker=ranker_preferred_mentee_initialization,
)


#################################
# PREFERRED RANKING, MENTOR POV #
#################################
ranker_preferred = pr.PairRankerMultiWithFavor(
    pair_rankers=[
        pr_pref_vs_rand,
        pr_mentor_yesnomaybe,
        pr_level_delta_minimize,
        pr_years_delta_minimize,
        pr_preferred_mentor_order,
        pr_preferred_mentor_count,
        pr_hash,
    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)
pair_ranker_context_manager.register(
    key=(PairType.PREFERRED, ApplicantType.MENTOR),
    pair_ranker=ranker_preferred,
)


##############################
# RANDOM RANKING, MENTEE POV #
##############################
WPR = pr.WeightedPairRanker
ranker_random_mentee_initialization = pr.PairRankerMultiWeighted(
    weighted_pair_rankers=[
        WPR(pr_mentee_yesnomaybe, 1),
        WPR(pr_skills_and_functions, 1),
        WPR(pr_level_delta_maximize, 1),
        WPR(pr_years_delta_maximize, 1),
        WPR(pr_hash, 0.1),            # TODO get pair's hash
    ],
)
pair_ranker_context_manager.register(
    key=(PairType.RANDOM, ApplicantType.MENTEE),
    pair_ranker=ranker_random_mentee_initialization,
)


##############################
# RANDOM RANKING, MENTOR POV #
##############################
ranker_random = pr.PairRankerMultiWithFavor(
    pair_rankers=[
        pr_pref_vs_rand,
        pr_mentor_yesnomaybe,
        pr_mentee_yesnomaybe,
        pr_level_delta_minimize,
        pr_years_delta_minimize,
        pr_skills_and_functions,
        pr_hash,
    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)
pair_ranker_context_manager.register(
    key=(PairType.RANDOM, ApplicantType.MENTOR),
    pair_ranker=ranker_random,
)
