import mentormatch.pair_compatibility as pc


class CompatibilityFactory:

    @staticmethod
    def random_match_compatibility() -> pc.pair_compatibility_abstract:
        randommatch_compatibility = pc.PairCompatibilityBuilder()
        randommatch_compatibility.register_pair_checkers([
            pc.PairCompatibilityNoPreference('mentor'),
            pc.PairCompatibilityNoPreference('mentee'),
            pc.PairCompatibilityYearsDelta(min_years_delta=7),
            pc.PairCompatibilityLevelDelta(),
            pc.PairCompatibilityNotSamePerson(),
        ])
        return randommatch_compatibility

    @staticmethod
    def preferred_match_compatibility() -> pc.pair_compatibility_abstract:
        prefmatch_compatibility = pc.PairCompatibilityBuilder()
        prefmatch_compatibility.register_pair_checkers([
            pc.PairCompatibilityNoPreference('mentor'),
            # pair_checker.PairCompatibilityNoPreference('mentee'),
            # pair_checker.PairCompatibilityYearsDelta(min_years_delta=7),
            # pair_checker.PairCompatibilityLevelDelta(),
            pc.PairCompatibilityNotSamePerson(),
        ])
