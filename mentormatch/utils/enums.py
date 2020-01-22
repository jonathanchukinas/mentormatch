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


# print(bool(YesNoMaybe.NO))


# cats = [YesNoMaybe.YES, YesNoMaybe.MAYBE, YesNoMaybe.NO]
# print([
#     item >= YesNoMaybe.MAYBE
#     for item in cats
# ])

# preference = {
#     YesNoMaybe.YES: 'happy',
#     YesNoMaybe.MAYBE: 'ok',
#     YesNoMaybe.NO: 'bad',
# }

# print(preference[YesNoMaybe.YES])
