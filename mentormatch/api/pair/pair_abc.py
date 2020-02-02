from mentormatch.api.utils.enums import ApplicantType
from abc import ABC, abstractmethod

# TODO get rid of ipair. I think i solved the problem with __futures_ annotations
class IPair(ABC):

    @abstractmethod
    def get_applicant(self, applicant_type: ApplicantType, return_other=False):  # pragma: no cover
        raise NotImplementedError
