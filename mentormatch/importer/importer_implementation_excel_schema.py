"""This module defines the fieldschema that the db and mentees worksheets
should contain."""
from fuzzytable import FieldPattern, cellpatterns as cp
from mentormatch.utils import ApplicantType
from mentormatch.utils.application_schema import ApplicationSchema


_application_schema = ApplicationSchema.get_schema()
_survey_question_aliases = ApplicationSchema.get_questions_and_aliases()
_selections = ApplicationSchema.get_selections()


class MentoringField(FieldPattern):
    # Wrapper around fuzzytable FieldPattern class

    def __init__(self, name, cellpattern=None, mentor_only=False, mentee_only=False, alias=None):
        self._applicable_to = {
            ApplicantType.MENTOR: not mentee_only,
            ApplicantType.MENTEE: not mentor_only
        }
        super().__init__(
            name=name,
            alias=_survey_question_aliases[name] if alias is None else alias,
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
        choices=_selections['gender'],
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
            choices=_selections['function'],
            case_sensitive=False,
            mode='approx',
    )),
    MentoringField(
        name='preferred_functions', mentee_only=True, cellpattern=cp.StringChoiceMulti(
            choices=_selections['function'],
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
            choices=_selections['max_mentee_count']
        ),
    ),
]

# TODO need to deal with 'null' in toml
# TODO add a check to see if mentee didn't seleect any random preferences.
#  This mentee gets excluded from random pairing

##########################
# YES/MAYBE/NO QUESTIONS #
#  (mentor and mentee)   #
##########################
for item in ApplicationSchema.get_locations_and_genders():
    _fieldschemas.append(MentoringField(name=item, alias=item, cellpattern=cp.StringChoice(
        choices=_selections['yesnomaybe'],
        dict_use_keys=False,
        default='no',
        case_sensitive=False,
        mode='approx',
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
