from typing import Type
from contextlib import contextmanager
from functools import lru_cache

from mentormatch.import_export.excel.excel_importer import ExcelImporter

# Applicants
from mentormatch.applicant import (
    Applicant, ApplicantCollection, Mentee, Mentor, ApplicantFactory
)

# Pairs
from mentormatch.pair.pair import Pair
from mentormatch.pair.pair_preferred import PreferredPair
from mentormatch.pair.pair_random import RandomPair

# Matcher
from mentormatch.matcher import Matcher

from mentormatch.initializer.initializer_abc import Initializer
from mentormatch.initializer.initializer_implementation import InitializerPreferred, \
    InitializerRandom

# Sorter
from .setup_sorter_context_mgr import sorter_context_manager  # TODO is this part of constructor for ...
# Initializer
# Matcher?

# Exporters
from mentormatch.import_export.exporter_base import BaseExporter
from mentormatch.import_export.exporter_multi import MultiExporter
from mentormatch.import_export.excel.excel_exporter import ExcelExporter
from mentormatch.import_export.toml.toml_exporter import TomlExporter

# Utils
from mentormatch.utils.enums import ApplicantType


class Factory:

    def __init__(self, mentee_dicts, mentor_dicts):
        self._applicant_dicts = {
            ApplicantType.MENTOR: mentor_dicts,
            ApplicantType.MENTEE: mentee_dicts,
        }
        self._applicants = {
            ApplicantType.MENTOR: self.get_collection(ApplicantType.MENTOR),
            ApplicantType.MENTEE: self.get_collection(ApplicantType.MENTEE),
        }
        self._wwid_pairs = []
        self._cfg = {}
        self._matching_type = None

    def get_pathgetter(self):
        # TODO this should be a class instead?
        from mentormatch.ui.selectfile import get_path

        def _pathgetter():
            self._cfg['path'] = get_path()
        return _pathgetter()

    def get_importer(self):
        return ExcelImporter(self._cfg['path'], self._mentor_dicts, self._mentee_dicts)

    def get_exporter(self) -> BaseExporter:
        exporter = MultiExporter()
        exporter.register_exporter(ExcelExporter(
            self._cfg['path'],
            self._mentor_dicts,
            self._mentee_dicts,
            self._wwid_pairs))
        exporter.register_exporter(TomlExporter(
            self._cfg['path'],
            self._mentor_dicts,
            self._mentee_dicts,
            self._wwid_pairs))
        return exporter

    @lru_cache
    def get_collection(self, applicant_type: ApplicantType) -> ApplicantCollection:
        return ApplicantCollection(
            applicant_dicts=self._applicant_dicts[applicant_type],
            applicant_factory=ApplicantFactory(sorter_context_manager),
        )

    def get_matcher(self) -> Matcher:
        with self._set_matching_type('preferred'):  # TODO replace with enum
            return self._get_matcher()

    def get_preferredmatcher(self) -> BaseMatcher:
        with self._set_matching_type('preferred'):  # TODO replace with enum
            return self._get_matcher()

    def get_randommatcher(self) -> BaseMatcher:
        with self._set_matching_type('random'):
            return self._get_matcher()

    def _get_matcher(self) -> BaseMatcher:
        if self._matching_type == 'preferred':  # TODO replace with enum
            matcher_constructor = PreferredMatcher
        elif self._matching_type == 'random':
            matcher_constructor = RandomMatcher
        else:
            raise ValueError
        return matcher_constructor(
            mentors=self._mentors,
            mentees=self._mentees,
            wwidpairs=self._wwid_pairs,
            pairs_builder=self._get_potential_pair_generator()
        )

    def _get_potential_pair_generator(self) -> Initializer:
        if self._matching_type == 'preferred':  # TODO replace with enum
            pairs_builder_constructors = InitializerPreferred
        elif self._matching_type == 'random':
            pairs_builder_constructors = InitializerRandom
        else:
            raise ValueError
        return pairs_builder_constructors(
            mentor_dicts=self._mentor_dicts,
            pair_constructor=self._get_pair_constructor()
        )

    @staticmethod
    def _get_applicant_constructor(applicant_type: str) -> Type[Applicant]:
        if applicant_type == 'mentor':  # TODO replace with enum
            return Mentor
        elif applicant_type == 'mentee':
            return Mentee
        else:
            raise ValueError

    def _get_pair_constructor(self) -> Type[Pair]:
        if self._matching_type == 'preferred':  # TODO replace with enum
            return PreferredPair
        elif self._matching_type == 'random':
            return RandomPair
        else:
            raise ValueError

    @contextmanager
    def _set_matching_type(self, matching_type):
        self._matching_type = matching_type
        yield
        self._matching_type = None
