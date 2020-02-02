"""This module defines the fieldschema that the db and mentees worksheets
should contain."""
from fuzzytable import FieldPattern, cellpatterns as cp
import toml
from pathlib import Path
from mentormatch.utils import ApplicantType
from mentormatch.utils import exceptions


# Get fieldschema from toml
_application_schema_path = Path(__file__).parent.parent.parent / "application_schema.toml"
_application_schema = toml.load(_application_schema_path)
_survey_question_aliases = dict(_application_schema['survey_questions']['with_alias']).update({
    fieldname: None
    for fieldname in _application_schema['survey_questions']['no_alias']
})
_selections = _application_schema['selections']


class MentoringField(FieldPattern):
    # Wrapper around fuzzytable FieldPattern class

    def __init__(self, name, cellpattern=None, mentor_only=False, mentee_only=False):
        self._applicable_to = {
            ApplicantType.MENTOR: not mentee_only,
            ApplicantType.MENTEE: not mentor_only
        }
        super().__init__(
            name=name,
            alias=_survey_question_aliases[name],
            mode='approx',
            min_ratio=0.5,
            cellpattern=cp.String if cellpattern is None else cellpattern,
            case_sensitive=False,
        )

    def applicable_to(self, _type: ApplicantType) -> bool:
        return self._applicable_to[_type]


_fieldschemas = [


    # BASIC BIO
    MentoringField("last_name"),
    MentoringField("first_name"),
    MentoringField("wwid", cp.Integer),
    MentoringField("nickname"),
    MentoringField("email_given"),
    MentoringField("job_title"),


    # EXPERIENCE
    MentoringField("position_level", cp.Digit),
    MentoringField("years_total", cp.Float),
    # MentoringField("years_jnj", cp.Float),


    # YES/NO/MAYBE
    # (appended down below)
    MentoringField("gender", cp.StringChoice(
        choices=_selections['genders'],
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx',
    )),
    MentoringField("location", cellpattern=cp.StringChoice(
        choices=_selections['location'],
        min_ratio=0.3,
        case_sensitive=False,
        mode='approx',
    )),


    # SKILLS
    MentoringField("skills", cellpattern=cp.StringChoiceMulti(
            choices=_selections['skill'],
            case_sensitive=False,
    )),


    # FUNCTION
    MentoringField('function', cellpattern=cp.StringChoice(
            choices=_selections['functions'],
            case_sensitive=False,
            mode='approx',
    )),
    MentoringField(
        name='preferred_functions', cellpattern=cp.StringChoiceMulti(
            choices=_selections['functions'],
            case_sensitive=False,
    )),


    # PREFERENCES
    MentoringField("preferred_wwids", cp.IntegerList, mentee_only=True),
    MentoringField(
        name="max_mentee_count",
        mentor_only=True,
        cellpattern=cp.StringChoice(
            dict_use_keys=False,
            mode='approx',
            choices=_selections['yesnomaybe']
        ),
    ),
]

##########################
# YES/MAYBE/NO QUESTIONS #
#  (mentor and mentee)   #
##########################
for item in _selections['locations'] + _selections['gender']:
    _fieldschemas.append(MentoringField(name=item, cellpattern=cp.StringChoice(
        choices=_selections['yesnomaybe'],
        dict_use_keys=False,
        default='no',
        case_sensitive=False,
        mode='approx'
    )))


fieldschemas = {}
for applicant_type in ApplicantType:
    fieldschemas[applicant_type] = [
        field
        for field in _fieldschemas
        if field.applicable_to(applicant_type)
    ]

# This is separate sheet in the excel workbook
# A mentee on this list is someone we really want to get paired this year.
# Usually, this is because they didn't get paired last year.
favor = [
    FieldPattern(name=fieldname, cellpattern=cp.Integer)
    for fieldname in 'wwid favor'.split()
]


# MentoringField.check_for_unused_toml_fields()
# selections.check_for_unused_toml_fields()
