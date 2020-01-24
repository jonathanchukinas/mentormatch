from enum import IntEnum


class ApplicantType(IntEnum):
    MENTOR = 2
    MENTEE = 1
    # Mentor is given higher number so that this expression resolves to True:
    # ApplicantType.MENTOR > ApplicantType.MENTEE


class YesNoMaybe(IntEnum):
    YES = 2
    MAYBE = 1
    NO = 0


class MinMax(IntEnum):
    MAX = 2
    MIN = 1
