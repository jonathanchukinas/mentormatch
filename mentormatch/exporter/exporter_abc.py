from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd


class Exporter(ABC):

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
