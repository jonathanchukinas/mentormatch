"""The Applicants object is a container of Applicant objects."""
from collections.abc import Iterable
from .applicant_abc import Applicant
from .applicant_null import ApplicantNotFound
from .applicant_factory import ApplicantFactory
from typing import Iterable


class ApplicantCollection(Iterable):

    def __init__(self, applicant_dicts, applicant_factory: ApplicantFactory):
        self._applicant_dicts = applicant_dicts
        self._applicant_factory = applicant_factory
        self._applicants = None
        self._wwid_dict = None

    def assemble_applicant_objects(self) -> None:
        self._applicants = [
            self._applicant_factory.build_applicant(applicant_dict)
            for applicant_dict in self._applicant_dicts
        ]
        self._wwid_dict = {
            applicant.wwid: applicant
            for applicant in self._applicants
        }

    def __iter__(self):
        yield from self._applicants

    # def __len__(self):
    #     return len(self._applicants)

    def get_applicant_by_wwid(self, wwid: int) -> Applicant:
        # TODO replace this with a group get
        # try:
        return self._wwid_dict[wwid]
        # except KeyError:
        #     return ApplicantNotFound()

        # TODO rand appl generator: add in posibiltty of choosing non-existent wwid

    def get_applicants_by_wwid(self, wwids: Iterable[int]) -> Iterable[Applicant]:
        return filter(None, (self._wwid_dict.get(wwid, None) for wwid in wwids))
        # return filter(applicants, )

