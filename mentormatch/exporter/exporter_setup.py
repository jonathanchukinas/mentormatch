from .exporter_aggregator import ExporterAggregator
from .exporter_abc import Exporter
import mentormatch.exporter.exporter_implementation as exim
from pathlib import Path


class ExporterFactory:

    def __init__(self, output_dir: Path):
        self._exporter = ExporterAggregator(exporters=[
            exim.ExporterTerminal(),
            exim.ExporterTxt(output_dir),
            exim.ExporterExcel(output_dir),
        ])

    def get_exporter(self) -> Exporter:
        return self._exporter
