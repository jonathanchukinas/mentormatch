from enum import IntEnum


class ApplicantType(IntEnum):
    MENTOR = 2
    MENTEE = 1
    # Mentor is given higher number so that this expression resolves to True:
    # ApplicantType.MENTOR > ApplicantType.MENTEE

    def get_other(self):
        if self is ApplicantType.MENTOR:
            return ApplicantType.MENTEE
        else:
            return ApplicantType.MENTOR


class YesNoMaybe(IntEnum):
    YES = 2
    MAYBE = 1
    NO = 0


class MinMax(IntEnum):
    MAX = 2
    MIN = 1


class PairType(IntEnum):
    PREFERRED = 2
    RANDOM = 1
