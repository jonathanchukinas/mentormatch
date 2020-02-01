from typing import List, Dict
from mentormatch.api.applicant import ApplicantCollection
from mentormatch.api.pair import Pair
from collections import defaultdict, Counter

# class MatchingSummary:
#
#     def __init__(self, applicants: ApplicantCollection):
#         self._applicants = applicants
#
#     def get_summary(self) -> List[Dict]:
#         pairs = []
#         for applicant in self._applicants:
#             pairs += list(applicant.yield_pairs)
#         return [
#             _convert_pair_to_dict(pair)
#             for pair in pairs
#         ]


class MatchingSummary:

    def __init__(self, mentors: ApplicantCollection, mentees: ApplicantCollection):
        self._mentors = mentors
        self._mentees = mentees

    def get_summary(self) -> List[Dict]:
        pairs = []
        for applicant in self._mentors:
            pairs += list(applicant.yield_pairs)
        return [
            _convert_pair_to_dict(pair)
            for pair in pairs
        ]

    def summarize_favor(self):
        favor_paired = Counter()
        favor_unpaired = Counter()
        for mentee in self._mentees:
            favor = mentee.application_dict['favor']
            paired = mentee.is_available


        single_favor_summary = defaultdict(dict)
        all_favor_summary = defaultdict(defaultdict(dict))



def _convert_pair_to_dict(pair: Pair) -> Dict:
    return {
        'mentor_wwid': pair.mentor.wwid,
        'mentee_wwid': pair.mentee.wwid,
        'pair_type': pair.pair_type.name.lower()
    }
