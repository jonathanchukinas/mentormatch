import mentormatch.pair_ranker as pr
from mentormatch.utils.enums import ApplicantType, YesNoMaybe, MinMax


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
# PREFERRED SETUP #
###################

ranker_preferred_mentee_initialization = pr_preferred_mentor_count

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


################
# RANDOM SETUP #
################

WPR = pr.WeightedPairRanker
ranker_random_mentee_initialization = pr.PairRankerMulti(
    pair_rankers=[
        WPR(pr_mentee_yesnomaybe, 1),
        WPR(pr_skills_and_functions, 1),
        WPR(pr_level_delta_maximize, 1),
        WPR(pr_years_delta_maximize, 1),
        WPR(pr_hash, 0.1),            # TODO get pair's hash
    ],
)

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
