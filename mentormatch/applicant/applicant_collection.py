"""The Applicants object is a container of Applicant objects."""

from mentormatch.applicant.applicant_abc import Applicant
from collections.abc import Sequence
from functools import lru_cache


class ApplicantCollection(Sequence):

    def __init__(self, applicant_dicts, applicant_constructor):
        self._applicant_dicts = applicant_dicts
        self._applicant_constructor = applicant_constructor
        self._applicant_objects = None

    def build_applicant_objects(self) -> None:

        self._applicant_objects = [
            self._applicant_constructor(applicant_dict)
            for applicant_dict in self._applicant_dicts
        ]

    def __len__(self):
        return len(self._applicant_objects)

    def __getitem__(self, item):
        return self._applicant_objects[item]

    def __iter__(self):
        yield from self._applicant_objects

    def get_applicant_by_wwid(self, wwid) -> Applicant:
        wwid_dict = self._get_wwid_dict()
        # TODO needs try/catch
        return wwid_dict[wwid]

    @lru_cache
    def _get_wwid_dict(self):
        return {
            applicant.wwid: applicant
            for applicant in self._applicant_objects
        }

    # def get_available_applicants(self):
    #     return list(filter(lambda applicant: applicant.is_available,
    # self._applicant_objects))
