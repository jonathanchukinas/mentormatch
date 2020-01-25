"""The Applicants object is a container of Applicant objects."""

from mentormatch.applicant.applicant_abc import Applicant
from collections.abc import Sequence
from functools import lru_cache


class ApplicantCollection(Sequence):

    def __init__(self, applicant_dicts, applicant_constructor):
        self._applicant_dicts = applicant_dicts
        self._applicant_constructor = applicant_constructor
        self._applicant_objects = None
        self._wwid_dict = None

    def build_applicant_objects(self) -> None:

        self._applicant_objects = [
            self._applicant_constructor(applicant_dict)
            for applicant_dict in self._applicant_dicts
        ]
        self._wwid_dict = {
            applicant.wwid: applicant
            for applicant in self._applicant_objects
        }

    def __len__(self):
        return len(self._applicant_objects)

    def __getitem__(self, item):
        return self._applicant_objects[item]

    def __iter__(self):
        yield from self._applicant_objects

    def get_applicant_by_wwid(self, wwid: int) -> Applicant:
        # TODO needs try/catch
        return self._wwid_dict[wwid]
