_mentor_dicts = []
_mentee_dicts = []
_wwid_pairs = []
_cfg = {}


def get_pathgetter():
    # TODO this should be a class instead?
    from mentormatch.ui.selectfile import get_path

    def _pathgetter():
        global _cfg
        _cfg['path'] = get_path()
    return _pathgetter()


def get_importer():
    from mentormatch.import_export.excel.excel_importer import ExcelImporter
    return ExcelImporter(_cfg['path'], _mentor_dicts, _mentee_dicts)


def get_exporter():
    from mentormatch.import_export.excel.excel_exporter import ExcelExporter
    return ExcelExporter(_cfg['path'], _mentor_dicts, _mentee_dicts, _wwid_pairs)


def get_collection_mentors():
    from mentormatch.applicants.collection_mentors import CollectionMentors
    return CollectionMentors(_mentor_dicts)


def get_collection_mentees():
    from mentormatch.applicants.collection_mentees import CollectionMentees
    return CollectionMentees(_mentee_dicts)


def get_preferredmatcher():
    pass


def get_randommatcher():
    pass
