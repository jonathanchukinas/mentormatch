from typing import List, Dict
from .setup_app_context import Context
from mentormatch.api.utils.enums import ApplicantType, PairType


def main(mentor_dicts: List[Dict], mentee_dicts: List[Dict]):

    context = Context(mentor_dicts, mentee_dicts)

    context.get_applicants(ApplicantType.MENTOR).assemble_applicant_objects()
    context.get_applicants(ApplicantType.MENTEE).assemble_applicant_objects()

    context.get_matcher(PairType.PREFERRED).execute()
    context.get_matcher(PairType.RANDOM).execute()

    return context.summarize_pairs()
