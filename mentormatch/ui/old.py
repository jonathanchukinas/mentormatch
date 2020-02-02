def get_pathgetter(self):
    from mentormatch.ui.selectfile import get_path

    def _pathgetter():
        self._cfg['path'] = get_path()

    return _pathgetter()


def get_importer(self):
    return ExcelImporter(self._cfg['path'], self._mentor_dicts, self._mentee_dicts)


def get_exporter(self) -> BaseExporter:
    exporter = MultiExporter()
    exporter.register_exporter(ExcelExporter(
        self._cfg['path'],
        self._mentor_dicts,
        self._mentee_dicts,
        self._wwid_pairs))
    exporter.register_exporter(TomlExporter(
        self._cfg['path'],
        self._mentor_dicts,
        self._mentee_dicts,
        self._wwid_pairs))
    return exporter