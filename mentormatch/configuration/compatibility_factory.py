from mentormatch import pair_compatibility


class CompatibilityFactory:

    @staticmethod
    def random_match_compatibility() -> pair_compatibility.pair_compatibility_abstract:
        randommatch_compatibility = pair_compatibility.PairCompatibilityBuilder()
        randommatch_compatibility.register_pair_checkers([
            pair_compatibility.PairCompatibilityNoPreference('mentor'),
            pair_compatibility.PairCompatibilityNoPreference('mentee'),
            pair_compatibility.PairCompatibilityYearsDelta(min_years_delta=7),
            pair_compatibility.PairCompatibilityLevelDelta(),
            pair_compatibility.PairCompatibilityNotSamePerson(),
        ])
        return randommatch_compatibility

    @staticmethod
    def preferred_match_compatibility() -> pair_compatibility.pair_compatibility_abstract:
        prefmatch_compatibility = pair_compatibility.PairCompatibilityBuilder()
        prefmatch_compatibility.register_pair_checkers([
            pair_compatibility.PairCompatibilityNoPreference('mentor'),
            # pair_checker.PairCompatibilityNoPreference('mentee'),
            # pair_checker.PairCompatibilityYearsDelta(min_years_delta=7),
            # pair_checker.PairCompatibilityLevelDelta(),
            pair_compatibility.PairCompatibilityNotSamePerson(),
        ])
