"""This module defines the fields that the db and mentees worksheets
should contain."""

# --- Standard Library Imports ------------------------------------------------
import collections

# --- Third Party Imports -----------------------------------------------------
from fuzzytable import FuzzyTable, FieldPattern, cellpatterns

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.worksheet import validation as v


class MentoringField(FieldPattern):
    def __init__(self, name, cellpattern=None, mentor_only=False, mentee_only=False):
        self.mentor_only = mentor_only
        self.mentee_only = mentee_only
        super().__init__(
            name,
            approximate_match=True,
            cellpattern=cellpattern,
        )


Field = collections.namedtuple(
    "Field",
    [
        "name",  # Header name
        "val_func",  # validation function. default: `convert_string`
        "mentor_only",  # Does this field apply only to db? default: False
        "mentee_only",  # Does this field apply only to mentees? default: False
        "error_txt",
    ],
)
Field.__new__.__defaults__ = (None, v.convert_string, False, False, False, None, None)




field_schema = [
    # Identification
    Field("first_name"),
    Field("last_name"),
    Field("wwid", v.convert_integer, error_txt="This cell requires an integer."),
    # Biography
    Field("gender"),
    Field("site"),
    Field("position_level", v.convert_first_digit_bw_2_6),
    Field("years", v.convert_float),
    # Preferences
    Field("genders_yes", v.convert_tuple_words),
    Field("genders_maybe", v.convert_tuple_words),
    Field("sites_yes", v.convert_tuple_words),
    Field("sites_maybe", v.convert_tuple_words),
    Field("max_mentee_count", v.convert_integer, mentor_only=True),
    Field("preferred_wwids", v.convert_tuple_ints, mentee_only=True),
    Field("wants_random_mentor", v.convert_boolean, mentee_only=True),
    # History
    Field("application_years", v.convert_tuple_ints, mentee_only=True),
    Field("participation_years", v.convert_tuple_ints, mentee_only=True),
]

fields = {
    "db": [field for field in field_schema if not field.mentee_only],
    "mentees": [field for field in field_schema if not field.mentor_only],
}


if __name__ == "__main__":
    pass
