import mentormatch.pair_ranker as pr
from mentormatch.utils.enums import ApplicantType, YesNoMaybe


pr_pref_vs_rand = pr.PairRankerPrefVsRand()
pr_mentor_yesnomaybe = pr.PairRankerLocationAndGender(
    ApplicantType.MENTOR, YesNoMaybe.YES)
pr_mentee_yesnomaybe = pr.PairRankerLocationAndGender(
    ApplicantType.MENTEE, YesNoMaybe.YES)
pr_level_delta = pr.PairRankerPositionLevel()
pr_years_delta = pr.PairRankerYearsExperience()
pr_preferred_mentor_count = pr.PairRankerPreferredMentorCount()
pr_preferred_mentor_order = pr.PairRankerPreferredMentorOrder()
pr_skills_and_functions = pr.PairRankerSkillsAndFunctions()
pr_favored = pr.PairRankerFavored()
pr_hash = pr.PairRankerHash()

ranker_preferred_mentee_initialization = pr_preferred_mentor_count

ranker_preferred = pr.PairRankerBuilder(
    pair_rankers=[
        pr_pref_vs_rand,
        pr_mentor_yesnomaybe,
        pr_level_delta,
        pr_years_delta,
        pr_preferred_mentor_order,
        pr_preferred_mentor_count,
        pr_hash,
    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)

# TODO: This needs a simpler class, one that doesn't involve favor
ranker_random_mentee_initialization = pr.PairRankerMulti(
    pair_rankers=[
        pr_mentee_yesnomaybe,
        pr_skills_and_functions,
        pr_level_delta,     # TODO flip this around
        pr_years_delta,     # TODO flip this around
        pr_hash,            # TODO get mentor's hash
    ],
)

ranker_random = pr.PairRankerBuilder(
    pair_rankers=[
        pr_pref_vs_rand,
        pr_mentor_yesnomaybe,
        pr_mentee_yesnomaybe,
        pr_level_delta,
        pr_years_delta,
        pr_skills_and_functions,
        pr_hash,
    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)
