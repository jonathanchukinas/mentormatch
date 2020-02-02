from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from collections import defaultdict
import pandas as pd  # TODO add to requires
if TYPE_CHECKING:
    from mentormatch.api.applicant.applicant_collection import ApplicantCollection


class MatchingSummary:

    def __init__(self, mentors: ApplicantCollection, mentees: ApplicantCollection):
        self._mentors = mentors
        self._mentees = mentees
        self.summary_dataframes: Dict[str, pd.DataFrame] = {}

    def summarize_all(self) -> None:
        self.add_pairs_to_dicts()
        dataframes = {
            'mentor_utilization': self.get_dataframe_mentor_utilization(),
            'favor': self.get_dataframe_favor(),
            'pairs': self.get_dataframe_pairs(),
        }
        self.summary_dataframes.update(dataframes)

    def get_dataframe_favor(self) -> pd.DataFrame:
        return pd.crosstab(
            rownames=['Favor Level'],
            index=(mentee.favor for mentee in self._mentees),
            colnames=['Is Paired?'],
            columns=(mentee.is_paired for mentee in self._mentees),
            margins=True,
            margins_name='Total'
        )

    def get_dataframe_mentor_utilization(self) -> pd.DataFrame:
        return pd.crosstab(
            rownames=['Actual'],
            index=(mentor.pair_count for mentor in self._mentors),
            colnames=['Max'],
            columns=(mentor.max_pair_count for mentor in self._mentors),
            margins=True,
            margins_name='Total'
        )

    def get_dataframe_pairs(self) -> pd.DataFrame:
        dict_pairs = defaultdict(list)
        for mentor in self._mentors:
            for pair in mentor.yield_pairs:
                mentee = pair.mentee
                dict_pairs['mentor_str'].append(str(mentor))
                dict_pairs['mentee_str'].append(str(mentee))
                dict_pairs['type'].append(pair.pair_type.name)
        df = pd.DataFrame(dict_pairs).set_index([
            'mentor_str',
            'mentee_str'
        ]).sort_index(level=[0, 1])
        return df.reset_index()

    def add_pairs_to_dicts(self) -> None:
        for applicants_collection in [self._mentors, self._mentees]:
            for applicant in applicants_collection:
                pairs = list(applicant.yield_pairs)
                matches = [
                    pair.get_applicant(applicant.applicant_type, return_other=True)
                    for pair in pairs
                ]
                wwids = [match.wwid for match in matches]
                match_types = [pair.pair_type.name for pair in pairs]
                applicant.application_dict['match_wwids'] = wwids  #if wwids else None
                applicant.application_dict['match_types'] = match_types  # if match_types else None
        for mentee in self._mentees:
            wwids = mentee.application_dict['match_wwids']
            if wwids:
                mentee.application_dict['match_wwids'] = int(wwids[0])
