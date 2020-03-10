from __future__ import annotations
from mentormatch.exporter.exporter_abc import Exporter
from typing import Dict, List
from pathlib import Path
import pandas as pd
import toml


# TODO I really should rework the exporter API since this class breaks the convention of only printing input or output.
class ExporterTxtPairDetails:

    def __init__(self, output_dir: Path, mentors: List[Dict], mentees: List[Dict]):
        self._path = output_dir / 'pair_details.txt'
        self._mentors = mentors
        self._mentees = {
            mentee['wwid']: mentee
            for mentee in mentees
        }

    def export(self) -> None:
        text_file_content = ''
        line = '\n' + '#'*30

        # Debug
        text_file_content += '\nstarting mentor count:\n' + str(len(self._mentors))
        text_file_content += '\nstarting mentee count:\n' + str(len(self._mentees))
        unpaired_mentor_count = 0
        unpaired_mentee_count = 0

        # Pairs
        unpaired_mentors = []
        for mentor in self._mentors:
            applicants = [mentor]
            for mentee_wwid in mentor['match_wwids']:
                applicants.append(self._mentees.pop(mentee_wwid))
            if len(applicants) == 1:
                unpaired_mentors.append(mentor)
                continue
            # Header            
            text_file_content += line
            for applicant in applicants:
                text_file_content += '\n' + self._get_name(applicant)
            text_file_content += line + '\n'
            # Applicant Dicts
            for applicant in applicants:
                text_file_content += '\n' + toml.dumps(applicant)

        # Unpaired Mentors
        unpaired_mentors = list(sorted(unpaired_mentors, key=lambda mentor: mentor['position_level'], reverse=True))
        text_file_content += line + '\nUNPAIRED MENTORS' + line + '\n'
        for mentor in unpaired_mentors:
            text_file_content += '\n' + toml.dumps(mentor)

        # Unpaired Mentees
        text_file_content += line + '\nUNPAIRED MENTEES' + line + '\n'
        for mentee in sorted(self._mentees.values(), key=lambda mentee: mentee['favor'], reverse=True):
            text_file_content += '\n' + toml.dumps(mentee)

        # Debug
        text_file_content = '\nunpaired mentor count:\n' + str(len(unpaired_mentors)) + '\nunpaired mentee count:\n' + str(len(self._mentees)) + text_file_content

        # Write to file
        self._path.write_text(text_file_content)

    def _get_name(self, applicant) -> str:
        return f"{applicant['first_name']} {applicant['last_name']} {applicant['wwid']}"
