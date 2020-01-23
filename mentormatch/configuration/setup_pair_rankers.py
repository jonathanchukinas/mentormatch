import mentormatch.pair_ranker as pr


ranker_random = pr.PairRankerBuilder(
    pair_rankers=[
        pr.PairRankerPrefVsRand(),
        pr.PairRankerHash(),
        pr.PairRankerFavored(),
        pr.PairRankerPreferredMentorCount(),
        pr.PairRankerPreferredMentorOrder(),  # THis is not the correct order
    ],
    pair_ranker_favor=pr.PairRankerFavored(),
    pair_ranker_favor_min_position=1,
)

ranker_random_mentee_initialization = pr.PairRankerBuilder(
    pair_rankers=[
        pr.PairRankerPrefVsRand(),
        pr.PairRankerHash(),
        pr.PairRankerFavored(),
        pr.PairRankerPreferredMentorCount(),
        pr.PairRankerPreferredMentorOrder(),  # THis is not the correct order
    ],
    pair_ranker_favor=pr.PairRankerFavored(),
    pair_ranker_favor_min_position=1,
)

ranker_preferred = pr.PairRankerBuilder(
    pair_rankers=[
        pr.PairRankerPrefVsRand(),
        pr.PairRankerHash(),
        pr.PairRankerFavored(),
        pr.PairRankerPreferredMentorCount(),
        pr.PairRankerPreferredMentorOrder(),  # THis is not the correct order
    ],
    pair_ranker_favor=pr.PairRankerFavored(),
    pair_ranker_favor_min_position=1,
)

ranker_preferred_mentee_initialization = None  # TODO make one for this.
