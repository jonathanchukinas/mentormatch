from enum import IntEnum


class ConversionMixin(IntEnum):

    def lower(self):
        return self.name.lower()

    @classmethod
    def get_enum(cls, value) -> 'YesNoMaybe':
        for enum in cls:
            if enum.lower() == value.lower():
                return enum
        raise ValueError


class ApplicantType(ConversionMixin, IntEnum):
    MENTOR = 2
    MENTEE = 1
    # Mentor is given higher number so that this expression resolves to True:
    # ApplicantType.MENTOR > ApplicantType.MENTEE

    def get_other(self):
        if self is ApplicantType.MENTOR:
            return ApplicantType.MENTEE
        else:
            return ApplicantType.MENTOR


class YesNoMaybe(ConversionMixin, IntEnum):
    YES = 2
    MAYBE = 1
    NO = 0

    def get_preference_key(self):
        return f'preference_{self.name.lower()}'


class MinMax(IntEnum):
    MAX = 2
    MIN = 1


class PairType(IntEnum):
    PREFERRED = 2
    RANDOM = 1

#
#
#
#
# for ynm in YesNoMaybe:
#     print(ynm.lower())
#     # print(ynm.name == 'NO')
