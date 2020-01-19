from mentormatch.matching.matching_abc import IMatcher


class PreferredMatcher(IMatcher):

    def generate_pairs(self):
        ###################
        # Collect Mentees #
        ###################
        all_mentees: List[Mentee] = list(self.applicants.mentees)
        mentees_available = [
            mentee
            for mentee in all_mentees
            if mentee.selected_preferred_mentors
        ]
        pairs_getter = potential_preferred_pairs

        perform_matching(
            mentees_available=mentees_available,
            pairs_getter=pairs_getter,
        )

    def get_wwidpairs(self):
        pass
