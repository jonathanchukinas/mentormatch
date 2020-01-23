from enum import IntEnum, Enum


class ApplicantType(IntEnum):
    MENTOR = 2
    MENTEE = 1
    # Mentor is given higher number so that this expression resolves to True:
    # ApplicantType.MENTOR > ApplicantType.MENTEE


class YesNoMaybe(Enum):
    YES = 2
    MAYBE = 1
    NO = 0

    def __gt__


print(YesNoMaybe.YES > YesNoMaybe.NO)
