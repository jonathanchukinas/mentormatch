from __future__ import annotations
from mentormatch.exporter.exporter_abc import Exporter
from typing import List, Dict
from pathlib import Path
import pandas as pd


class ExporterAggregator(Exporter):

    def __init__(self, exporters: List[Exporter]):
        self._exporters = exporters

    def export_results(self, results: Dict[str, pd.DataFrame]) -> None:
        for exporter in self._exporters:
            exporter.export_results(results)

    def export_inputs(self, mentors: List[Dict], mentees: List[Dict]) -> None:
        for exporter in self._exporters:
            exporter.export_inputs(mentors, mentees)
