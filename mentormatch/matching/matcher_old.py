from mentormatch.matching.matcher_base import BaseMatcher


class PreferredMatcher(BaseMatcher):

    def run(self):
        ###################
        # Collect Mentees #
        ###################
        all_mentees: List[Mentee] = list(self.applicants.mentees)
        mentees_available = [
            mentee
            for mentee in all_mentees
            if mentee.selected_at_least_one_preferred_mentor
        ]
        pairs_getter = potential_preferred_pairs

        perform_matching(
            mentees_available=mentees_available,
            pairs_getter=pairs_getter,
        )


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