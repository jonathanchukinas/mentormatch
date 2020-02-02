from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from mentormatch.utils import ApplicantType


class Importer(ABC):

    @abstractmethod
    def execute(self) -> Dict[ApplicantType, List[Dict]]:
        raise NotImplementedError
