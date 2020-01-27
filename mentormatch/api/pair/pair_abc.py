from mentormatch.api.utils.enums import ApplicantType
from abc import ABC, abstractmethod


class IPair(ABC):

    @abstractmethod
    def get_applicant(self, applicant_type: ApplicantType, return_other=False):  # pragma: no cover
        raise NotImplementedError
