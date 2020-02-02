from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from typing import Dict, List


class Exporter(ABC):

    # def __init__(self, output_dir: Path):
    #     self._output_dir = output_dir

    @abstractmethod
    def export_results(self,
                       results: Dict[str, pd.DataFrame]
                       ) -> None:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def export_inputs(self,
                      mentors: List[Dict],
                      mentees: List[Dict]
                      ) -> None:  # pragma: no cover
        raise NotImplementedError
