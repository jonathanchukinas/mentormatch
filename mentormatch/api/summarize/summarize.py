from typing import List, Dict
from mentormatch.api.applicant import ApplicantCollection
from mentormatch.api.pair import Pair


class MatchingSummary:

    def __init__(self, applicants: ApplicantCollection):
        self._applicants = applicants

    def get_summary(self) -> List[Dict]:
        pairs = []
        for applicant in self._applicants:
            pairs += list(applicant.yield_pairs)
        return [
            _convert_pair_to_dict(pair)
            for pair in pairs
        ]


def _convert_pair_to_dict(pair: Pair) -> Dict:
    return {
        'mentor_wwid': pair.mentor.wwid,
        'mentee_wwid': pair.mentee.wwid,
        'pair_type': pair.pair_type.name.lower()
    }
