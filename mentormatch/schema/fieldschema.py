"""This module defines the fieldschema that the db and mentees worksheets
should contain."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
from fuzzytable import FieldPattern, cellpatterns as cp

# --- Intra-Package Imports ---------------------------------------------------
# None


class MentoringField(FieldPattern):
    def __init__(self, name, cellpattern=None, alias=None, mentor_only=False, mentee_only=False):
        self.mentor_only = mentor_only
        self.mentee_only = mentee_only
        super().__init__(
            name=name,
            alias=alias,
            approximate_match=True,
            min_ratio=0.5,
            cellpattern=cp.String if cellpattern is None else cellpattern,
        )


MF = MentoringField
_fieldschema = [
    # Biography
    MF("first_name"),
    MF("nickname"),
    MF("last_name"),
    MF("gender"),
    MF("wwid", cp.Integer),
    MF("email_given", alias="J&J Email Address"),
    MF("job_title"),
    MF("department", alias="department and or job function"),
    MF("site", alias="which is your home office"),  # TODO normalize with official site list
    MF("years_total", cp.Float, alias="years of experience"),
    MF("years_jnj", cp.Float, alias="years with jnj"),
    MF("position_level", cp.Digit),
    # Preferred WWIDS
    MF("preferred_wwids", cp.IntegerList, alias="wwids of preferred mentors", mentee_only=True),
    # Mentor
    MF("max_mentee_count", cp.Integer, mentor_only=True),
]

##########################
# YES/MAYBE/NO QUESTIONS #
#  (mentor and mentee)   #
##########################

locations = [
    'fort_washington',
    'malvern',
    'spring_house',
    'west_chester',
    'horsham',
    'titusville',
]
genders = [
    'female',
    'male',
]

choices_yesnomaybe = {
    'yes': 'Yes',  # 'Definitely Yes'   # TODO change to the actual output of the MS Forms
    'maybe': 'preference',  # 'Not my first preference, but I'd make it work'
    'no': 'No',  # 'No'  # TODO fuzzytable v0.16 change to stringchoice: case insensitive
}

for item in locations + genders:
    _fieldschema.append(MF(
        name=item,
        cellpattern=cp.StringChoice(choices=choices_yesnomaybe, dict_use_keys=False, default='no'),
    ))

#################
# MENTOR SKILLS #
# (mentee only) #
#################
# TODO add to pipeline script: exit virtualenv
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
favored = [
    FieldPattern(name=fieldname, cellpattern=cp.Integer)
    for fieldname in 'wwid favor'.split()
]

if __name__ == "__main__":
    pass
