"""This module defines the fieldschema that the db and mentees worksheets
should contain."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
from fuzzytable import FieldPattern, cellpatterns as cp

# --- Intra-Package Imports ---------------------------------------------------
# None


# TODO implement new category that I discussed with Paige


class MentoringField(FieldPattern):
    def __init__(self, name, cellpattern=None, alias=None, mentor_only=False, mentee_only=False):
        self.mentor_only = mentor_only
        self.mentee_only = mentee_only
        super().__init__(
            name=name,
            alias=alias,
            mode='approx',
            min_ratio=0.5,
            cellpattern=cp.String if cellpattern is None else cellpattern,
            case_sensitive=False,
        )

genders = [
    'female',
    'male',
]

locations = [
    'fort_washington',
    'malvern',
    'spring_house',
    'west_chester',
    'horsham',
    # 'titusville',  # TODO remove titusville from mentee application
    # TODO remove "skill prefix" from mentee preferences.
]


MF = MentoringField
_fieldschema = [
    # Biography
    MF("first_name"),
    MF("nickname"),
    MF("last_name"),
    MF("gender", cp.StringChoice(
        choices=genders,
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx'
    )),
    MF("wwid", cp.Integer),
    MF("email_given", alias="J&J Email Address"),
    MF("job_title"),
    MF("department", alias="department and or job function"),
    MF("location", alias="which is your home office", cellpattern=cp.StringChoice(
        choices=locations,
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx'
    )),
    MF("years_total", cp.Float, alias="years of experience"),
    MF("years_jnj", cp.Float, alias="years with jnj"),
    MF("position_level", cp.Digit),
    # Preferred WWIDS
    MF("preferred_wwids", cp.IntegerList, alias="wwids of preferred mentors", mentee_only=True),
    # Mentor
    MF(
        name="max_mentee_count",
        cellpattern=cp.StringChoice(dict_use_keys=False, mode='approx', choices={
            1: 'One mentee only, please!',
            2: "I'm willing to take on two mentees.",
            3: "I can handle this! Give me three mentees.",
        }),
        mentor_only=True,
        alias='How many mentees are you willing to mentor?'
    ),
]

##########################
# YES/MAYBE/NO QUESTIONS #
#  (mentor and mentee)   #
##########################

choices_yesnomaybe = {
    'yes': 'Definitely Yes',
    'no': 'No',
    'maybe': "Not my first preference, but I'd make it work.",
}

for item in locations + genders:
    _fieldschema.append(MF(
        name=item,
        cellpattern=cp.StringChoice(
            choices=choices_yesnomaybe,
            dict_use_keys=False,
            default='no',
            case_sensitive=False,
            mode='approx'
        ),
    ))

#################
# MENTOR SKILLS #
# (mentee only) #
#################
mentor_skills = [
    'public speaking',
    'managing up',
    'large career shifts',
]
_fieldschema.append(MF(
    name="mentor_skills",
    cellpattern=cp.StringChoiceMulti(
        choices=mentor_skills,
        case_sensitive=False,
    ),
    alias="which of these mentor skills are important to you",
    mentee_only=True,
))


fieldschemas = {
    "mentors": [field for field in _fieldschema if not field.mentee_only],
    "mentees": [field for field in _fieldschema if not field.mentor_only],
}

# This is separate sheet in the excel workbook
# A mentee on this list is someone we really want to get paired this year.
# Usually, this is because they didn't get paired last year.
favor = [
    FieldPattern(name=fieldname, cellpattern=cp.Integer)
    for fieldname in 'wwid favor'.split()
]

if __name__ == "__main__":
    pass
