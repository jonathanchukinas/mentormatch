from mentormatch.pair.pair_base import Pair
from mentormatch.pair_ranker.util import PairsEqual


class PairComparison:

    def __init__(self, self_pair: Pair, other_pair: Pair):
        self.self_pair = self_pair
        self.other_pair = other_pair
        self.pairs = [self_pair, other_pair]

    def get_better_pair(self) -> Pair:

        # TODO preferred comparison
        if self.self_pair.preferred and self.other_pair.random:
            return self.self_pair
        elif self.self_pair.random and self.other_pair.preferred:
            return self.other_pair
        elif self.self_pair.preferred and self.self_pair.preferred:
            compare_funcs = [
                # self.preferred_vs_random,
                self.location_and_gender_mentor,
                self.level_delta,
                self.years_delta,
                self.rank_order,  # Preferred Only
                self.wwid_count,  # Preferred Only
                self.hashorder,
            ]
        elif self.self_pair.random and self.self_pair.random:
            compare_funcs = [
                # self.preferred_vs_random,
                self.location_and_gender_mentor,
                self.location_and_gender_mentee,  # Random only
                self.level_delta,
                self.years_delta,
                self.hashorder,
            ]
        else:
            raise ValueError  # pragma: no cover

        ###################
        # Favored Mentees #
        ###################
        restart_count = max(pair.mentee.restart_count for pair in self.pairs)
        # TODO max restart needs to reset when switching over to random pairing.
        insert_index = -(1 + restart_count)  # always occurs before hashorder, an unfair arbitrary metric
        min_allowed_insert_index = 1 - len(compare_funcs)  # should never occur before pref-vs-random
        insert_index = max(min_allowed_insert_index, insert_index)  # make sure it's never out of range
        compare_funcs.insert(insert_index, self.favored)

        #######################
        # Execute comparisons #
        #######################
        for func in compare_funcs:
            better_pair = func()
            if better_pair is PairsEqual:
                # It's a tie. Go to next comparison function
                continue
            else:
                return better_pair
        raise ValueError("One of these pairs should have been better than the other!")  # pragma: no cover

    def _better_pair(self, _list, min_mode=False):
        if _list[0] == _list[1]:
            return PairsEqual
        minmax_func = min if min_mode else max
        best_index = _list.index(minmax_func(_list))
        return self.pairs[best_index]

    # def preferred_vs_random(self):
    #     scoring = {'preferred': 1, 'random': 0}
    #     scores = [
    #         scoring[pair.match_type]
    #         for pair in self.pairs
    #     ]
    #     better_pair = self._better_pair(scores)
    #     return better_pair
