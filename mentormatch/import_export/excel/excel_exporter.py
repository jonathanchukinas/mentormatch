class ExcelExporter:

    def __init__(self, path, mentor_dicts, mentee_dicts, wwid_pairs):
        self.mentor_dicts = mentor_dicts
        self.mentee_dicts = mentee_dicts
        self.path = path
        self.wwid_pairs = wwid_pairs
