from mentormatch.import_export.exporter_base import BaseExporter


class TomlExporter(BaseExporter):

    def __init__(self, path, mentor_dicts, mentee_dicts, wwid_pairs):
        self.mentor_dicts = mentor_dicts
        self.mentee_dicts = mentee_dicts
        self.path = path
        self.wwid_pairs = wwid_pairs

    def export(self):

        # First two dictionaries: mentors and mentees
        results_dict = {}  # keys: mentors/ees
        for groupname, applicants in self.items():
            group_dict = {
                str(applicant): dict(applicant)
                for applicant in applicants
            }
            results_dict[groupname] = group_dict

        # Third dictionary: pairs as wwids
        # key: mentor wwid
        # value: list of mentee wwids
        pairs = {}
        results_dict['pairs'] = pairs
        for mentor in self.mentors:
            mentor_wwid = str(mentor.wwid)
            mentor_pairedmenteewwids = [
                pair.mentee.wwid
                for pair in mentor.assigned_pairs
            ]
            pairs[mentor_wwid] = mentor_pairedmenteewwids

        # Write dicts to toml
        applicants_tomlstring = toml.dumps(results_dict)
        toml_path = self.excel_path.parent / "matching_results.toml"
        toml_path.touch()
        with open(toml_path, "w") as f:
            f.write(applicants_tomlstring)
