import mentormatch.api.compatibility as pc
from mentormatch.utils import ApplicantType, PairType

#########################
# COMPATIBILITY FACTORY #
#########################
compatibility_factory = pc.CompatibilityCheckerFactory()


#############
# PREFERRED #
#############
_compatibility_checker_preferred = pc.CompatibilityAggregator()
_compatibility_checker_preferred.register_pair_checkers([
    # pc.CompatibilityApplicantNotFound(),
    pc.CompatibilityNoPreference(ApplicantType.MENTOR),
    pc.CompatibilityNotSamePerson(),
])
compatibility_factory.register(
    pair_type=PairType.PREFERRED,
    compatibility_checker=_compatibility_checker_preferred,
)


##########
# RANDOM #
##########
_compatibility_checker_random = pc.CompatibilityAggregator()
_compatibility_checker_random.register_pair_checkers([
    pc.CompatibilityRandomMentee(),
    pc.CompatibilityNoPreference(ApplicantType.MENTOR),
    pc.CompatibilityNoPreference(ApplicantType.MENTEE),
    pc.CompatibilityYearsDelta(min_years_delta=7),
    pc.CompatibilityLevelDelta(),
    pc.CompatibilityNotSamePerson(),
])
compatibility_factory.register(
    pair_type=PairType.RANDOM,
    compatibility_checker=_compatibility_checker_random,
)
