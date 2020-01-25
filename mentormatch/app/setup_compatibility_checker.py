import mentormatch.compatibility_checker as pc
from mentormatch.utils.enums import ApplicantType, PairType

#########################
# COMPATIBILITY FACTORY #
#########################
compatibility_factory = pc.CompatibilityCheckerFactory()

#############
# PREFERRED #
#############
_compatibility_checker_preferred = pc.CompatibilityCheckerAggregator()
_compatibility_checker_preferred.register_pair_checkers([
    pc.CompatibilityCheckerNoPreference(ApplicantType.MENTOR),
    pc.CompatibilityCheckerNotSamePerson(),
])
compatibility_factory.register(
    pair_type=PairType.PREFERRED,
    compatibility_checker=_compatibility_checker_preferred,
)

##########
# RANDOM #
##########
_compatibility_checker_random = pc.CompatibilityCheckerAggregator()
_compatibility_checker_random.register_pair_checkers([
    pc.CompatibilityCheckerNoPreference(ApplicantType.MENTOR),
    pc.CompatibilityCheckerNoPreference(ApplicantType.MENTEE),
    pc.CompatibilityCheckerYearsDelta(min_years_delta=7),
    pc.CompatibilityCheckerLevelDelta(),
    pc.CompatibilityCheckerNotSamePerson(),
])
compatibility_factory.register(
    pair_type=PairType.RANDOM,
    compatibility_checker=_compatibility_checker_random,
)
