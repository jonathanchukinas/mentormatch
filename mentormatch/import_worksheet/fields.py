"""This module defines the fields that the db and mentees worksheets
should contain."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
from fuzzytable import FieldPattern, cellpatterns as cp

# --- Intra-Package Imports ---------------------------------------------------
# None


class MentoringField(FieldPattern):
    def __init__(self, name, cellpattern=None, mentor_only=False, mentee_only=False):
        self.mentor_only = mentor_only
        self.mentee_only = mentee_only
        super().__init__(
            name,
            approximate_match=True,
            cellpattern=cp.String if cellpattern is None else cellpattern,
        )


MF = MentoringField
field_schema = [
    # Identification
    MF("first_name"),
    MF("last_name"),
    MF("wwid", cp.Integer),
    # Biography
    MF("gender"),
    MF("site"),
    MF("position_level"),  # TODO need to extract the first digit?
    MF("years", cp.Float),
    # Preferences
    MF("genders_yes", cp.WordList),  # TODO need cp.WordList
    MF("genders_maybe", cp.WordList),
    MF("sites_yes", cp.WordList),
    MF("sites_maybe", cp.WordList),
    MF("max_mentee_count", cp.Integer, mentor_only=True),
    MF("preferred_wwids", cp.IntegerList, mentee_only=True),
    MF("wants_random_mentor", cp.Boolean, mentee_only=True),  # TODO need cp.Boolean
    # History
    MF("application_years", cp.IntegerList, mentee_only=True),
    MF("participation_years", cp.IntegerList, mentee_only=True),
]

fields = {
    "mentors": [field for field in field_schema if not field.mentee_only],
    "mentees": [field for field in field_schema if not field.mentor_only],
}


if __name__ == "__main__":
    pass
