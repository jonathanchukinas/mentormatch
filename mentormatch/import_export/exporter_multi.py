from mentormatch.import_export.exporter_base import BaseExporter
from typing import List, Type


class MultiExporter(BaseExporter):

    def __init__(self):
        self._exporters: List[BaseExporter] = []

    def register_exporter(self, exporter_object: BaseExporter):
        self._exporters.append(exporter_object)

    def export(self):
        for exporter in self._exporters:
            exporter.export()
