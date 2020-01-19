from mentormatch.matching.matcher_base import BaseMatcher


class RandomMatcher(BaseMatcher):

    def run(self):
        ###################
        # Collect Mentors #
        ###################
        mentors_available = filter(lambda m: m.below_capacity, self.applicants.mentors)
        mentors_available = tuple(sorted(mentors_available, key=lambda m: m.hash))
        pairs_getter = PotentialRandomPairCreator(mentors_available).get_pairs

        ###################
        # Collect Mentees #
        ###################
        mentees_available = list(filter(lambda m: not m.paired, self.applicants.mentees))

        perform_matching(
            mentees_available=mentees_available,
            pairs_getter=pairs_getter,
        )
