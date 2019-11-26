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

# TODO implement case insensitive


# TODO need schema for "favored". That should be a separate spreadsheet.

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

yes_maybe_no =[
    'fort_washington',
    'malvern',
    'spring_house',
    'west_chester',
    'horsham',
    'titusville',
    'gender_female',
    'gender_male',
]
for item in yes_maybe_no:
    _fieldschema.append(MF(
        name=item,
        cellpattern=cp.String,  # TODO replace this with a custom parser
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
    cellpattern=cp.String,  # TODO implement custom parser
    alias="which of these mentor skills are important to you",
    mentee_only=True,
))



fieldschema = {
    "mentors": [field for field in _fieldschema if not field.mentee_only],
    "mentees": [field for field in _fieldschema if not field.mentor_only],
}


if __name__ == "__main__":
    pass
