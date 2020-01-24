import mentormatch.pair_ranker as pr


pr_pref_vs_rand = pr.PairRankerPrefVsRand()
pr_hash = pr.PairRankerHash()
pr_favored = pr.PairRankerFavored()
pr_preferred_mentor_count = pr.PairRankerPreferredMentorCount()
pr_preferred_mentor_order = pr.PairRankerPreferredMentorOrder()


ranker_random = pr.PairRankerBuilder(
    pair_rankers=[
          # THis is not the correct order
    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)

ranker_random_mentee_initialization = pr.PairRankerBuilder(
    pair_rankers=[

    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)

ranker_preferred = pr.PairRankerBuilder(
    pair_rankers=[

    ],
    pair_ranker_favor=pr_favored,
    pair_ranker_favor_min_position=1,
)

ranker_preferred_mentee_initialization = pr_preferred_mentor_count
