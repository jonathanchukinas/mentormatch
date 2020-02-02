"""This module defines the fieldschema that the db and mentees worksheets
should contain."""
from fuzzytable import FieldPattern, cellpatterns as cp
import toml
from pathlib import Path


# Get fieldschema from toml
_application_schema_path = Path(__file__).parent.parent.parent / "application_schema.toml"
_application_schema = toml.load(_application_schema_path)


class MentoringField(FieldPattern):
    # Wrapper around fuzzytable FieldPattern class

    # TODO why is this a class attr?  Can it be moved external to the class?
    survey_question_aliases = dict(_application_schema['survey_questions']['with_alias']).update({
        fieldname: None
        for fieldname in _application_schema['survey_questions']['no_alias']
    })

    def __init__(self, name, cellpattern=None, mentor_only=False, mentee_only=False):
        self.mentor_only = mentor_only
        self.mentee_only = mentee_only
        alias = self.get_alias(name)
        super().__init__(
            name=name,
            alias=alias,
            mode='approx',
            min_ratio=0.5,
            cellpattern=cp.String if cellpattern is None else cellpattern,
            case_sensitive=False,
        )

    @classmethod
    def get_alias(cls, field_name):
        try:
            return cls.survey_question_aliases.pop(field_name)
        except KeyError:
            raise exceptions.MissingFieldschemaError('survey_questions', field_name)  # TODO make sure these generate an error

    @classmethod
    def check_for_unused_toml_fields(cls):
        unused_fieldnames = list(cls.survey_question_aliases.keys())
        if len(unused_fieldnames) > 0:
            raise exceptions.UnusedFieldschemaError('survey_questions', unused_fieldnames)


class Selections:

    def __init__(self):
        self._selections = dict(toml_schema['selections'])
        self._used_selections = set()

    def __getattr__(self, item):
        self._used_selections.add(item)
        try:
            self._selections.pop(item)
        except KeyError:
            raise exceptions.MissingFieldschemaError('selections', item)  # TODO make sure these generate an error

    def check_for_unused_toml_fields(self):  # TODO make sure these generate an error
        unused_selections = list(set(self._selections.keys()) - set(self._used_selections))
        if len(unused_selections) > 0:
            raise exceptions.UnusedFieldschemaError('survey_questions', unused_selections)


selections = Selections()


MF = MentoringField
_fieldschema = [
    MF("first_name"),
    MF("nickname"),
    MF("last_name"),
    MF("gender", cp.StringChoice(
        choices=selections.genders,
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx'
    )),
    MF("wwid", cp.Integer),
    MF("email_given"),
    MF("job_title"),
    MF("department_self"),
    MF("department_preference", mentee_only=True),
    MF("location", cellpattern=cp.StringChoice(
        choices=selections.locations,
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx'
    )),
    MF("years_total", cp.Float),
    MF("years_jnj", cp.Float),
    MF("position_level", cp.Digit),
    MF("preferred_wwids", cp.IntegerList, mentee_only=True),
    MF("max_mentee_count", mentor_only=True, cellpattern=cp.StringChoice(
            dict_use_keys=False,
            mode='approx',
            choices=selections.yesnomaybe),
    ),
]

##########################
# YES/MAYBE/NO QUESTIONS #
#  (mentor and mentee)   #
##########################
for item in selections.locations + selections.genders:
    _fieldschema.append(MF(name=item, cellpattern=cp.StringChoice(
        choices=selections.yesnomaybe,
        dict_use_keys=False,
        default='no',
        case_sensitive=False,
        mode='approx'
    )))

#################
# MENTOR SKILLS #
# (mentee only) #
#################
_fieldschema.append(MF(
    name="mentor_skills",
    cellpattern=cp.StringChoiceMulti(
        choices=selections.mentor_skills,
        case_sensitive=False,
    ),
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


MentoringField.check_for_unused_toml_fields()
selections.check_for_unused_toml_fields()
