from __future__ import annotations
from mentormatch.exporter.exporter_abc import Exporter
from typing import Dict, List
from pathlib import Path
import pandas as pd
import toml


class ExporterExcel(Exporter):

    def __init__(self, output_dir: Path):
        self._path = output_dir / 'results.xlsx'

    def export_inputs(self, mentors: List[Dict], mentees: List[Dict]) -> None:
        applicants_dicts = {
            'mentor': _applicantslistdicts_to_dataframe(mentors),
            'mentee': _applicantslistdicts_to_dataframe(mentees),
        }
        self._write_to_excel(applicants_dicts)

    def export_results(self, results: Dict[str, pd.DataFrame]) -> None:
        self._write_to_excel(results)

    def _write_to_excel(self, dict_of_dataframes: Dict[str, pd.DataFrame]) -> None:
        with pd.ExcelWriter(
            path=str(self._path),
            mode=_get_file_write_mode(self._path)
        ) as writer:
            for title, df in dict_of_dataframes.items():
                df.to_excel(excel_writer=writer, sheet_name=title.title())


class ExporterTerminal(Exporter):

    def export_inputs(self, mentors: List[Dict], mentees: List[Dict]) -> None:
        applicants_dicts = {
            'mentor': _get_first_and_last_applicants(mentors),
            'mentee': _get_first_and_last_applicants(mentees),
        }
        print(_build_applicants_report_string(applicants_dicts))

    def export_results(self, results: Dict[str, pd.DataFrame]) -> None:
        print(_build_results_string(results))


class ExporterTxt(Exporter):

    def __init__(self, output_dir: Path):
        self._path = output_dir / 'output.txt'

    def export_inputs(self, mentors: List[Dict], mentees: List[Dict]) -> None:
        applicants_dicts = {
            'mentor': mentors,
            'mentee': mentees,
        }
        _str = _build_applicants_report_string(applicants_dicts)
        self._write(_str)

    def export_results(self, results: Dict[str, pd.DataFrame]) -> None:
        self._write(_build_results_string(results, print_all_rows=True))

    def _write(self, _str) -> None:
        self._path.parent.mkdir(exist_ok=True, parents=True)
        self._path.write_text(_str)


def _build_results_string(results: Dict[str, pd.Dataframe], print_all_rows=False) -> str:
    _str = '\n\nRESULTS\n\n\n'
    for title, dataframe in results.items():
        dataframe: pd.DataFrame
        _str += f"{title.upper().replace('_', ' ')}\n"
        if print_all_rows:
            _str += dataframe.to_string()
        else:
            _str += str(dataframe)
        _str += '\n\n\n'
    return _str


def _build_applicants_report_string(applicants: Dict[str, List[Dict]]) -> str:
    _str = '\n\nEXAMPLES OF IMPORTED MENTORS AND MENTEES:\n\n'
    _str += _dict_to_toml(applicants)
    return _str


def _get_first_and_last_applicants(applicants: List[Dict]) -> List[Dict]:
    first = min(applicants, key=lambda a: a['last_name'])
    last = max(applicants, key=lambda a: a['last_name'])
    return [first, last]


# class ExporterToml(Exporter):
#
#     def export_results(self):
#
#         # First two dictionaries: mentors and mentees
#         results_dict = {}  # keys: mentors/ees
#         for groupname, applicants in self.items():
#             group_dict = {
#                 str(applicant): dict(applicant)
#                 for applicant in applicants
#             }
#             results_dict[groupname] = group_dict
#
#         # Third dictionary: pairs as wwids
#         # key: mentor wwid
#         # value: list of mentee wwids
#         pairs = {}
#         results_dict['pairs'] = pairs
#         for mentor in self.mentors:
#             mentor_wwid = str(mentor.wwid)
#             mentor_pairedmenteewwids = [
#                 pair.mentee.wwid
#                 for pair in mentor.assigned_pairs
#             ]
#             pairs[mentor_wwid] = mentor_pairedmenteewwids
#
#         # Write dicts to toml
#         applicants_tomlstring = toml.dumps(results_dict)
#         toml_path = self.excel_path.parent / "matching_results.toml"
#         toml_path.touch()
#         with open(toml_path, "w") as f:
#             f.write(applicants_tomlstring)
#
#     def export_inputs(self, mentors: List[Dict], mentees: List[Dict]) -> None:
#         raise NotImplementedError

def _applicantslistdicts_to_dataframe(list_of_dicts: List[Dict]) -> pd.DataFrame:
    _dict = {}
    for key in list_of_dicts[0].keys():
        _dict[key] = []
    for applicant in list_of_dicts:
        for key, value in applicant.items():
            value = value if value else None
            _dict[key].append(value)
    return pd.DataFrame(_dict)


def _dict_to_toml(value):
    return toml.dumps(value)


def _get_file_write_mode(path: Path):
    if path.exists():
        return 'a'
    else:
        return 'w'
