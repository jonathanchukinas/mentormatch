from typing import Type
from contextlib import contextmanager
from functools import lru_cache

from mentormatch.import_export.excel.excel_importer import ExcelImporter

# Applicants
from mentormatch.applicants import (
    ApplicantBase, ApplicantCollection, Mentee, Mentor
)

# Pairs
from mentormatch.pair.pair_base import Pair
from mentormatch.pair.pair_preferred import PreferredPair
from mentormatch.pair.pair_random import RandomPair

# Matching
from mentormatch.pairs_initializer.pairs_initializer import PairsInitializer
from mentormatch.pairs_initializer.pairs_initializer_preferred import PreferredPairsInitializer
from mentormatch.pairs_initializer.pairs_initializer_random import RandomPairsInitializer
from mentormatch.matching.matcher_base import BaseMatcher
from mentormatch.matching.matcher_preferred import PreferredMatcher
from mentormatch.matching.matcher_random import RandomMatcher

# Exporters
from mentormatch.import_export.exporter_base import BaseExporter
from mentormatch.import_export.exporter_multi import MultiExporter
from mentormatch.import_export.excel.excel_exporter import ExcelExporter
from mentormatch.import_export.toml.toml_exporter import TomlExporter


class Factory:

    def __init__(self):
        self._mentor_dicts = []
        self._mentee_dicts = []
        self._mentors = self.get_collection_mentors()
        self._mentees = self.get_collection_mentees()
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
    def get_collection_mentors(self) -> ApplicantCollection:
        return applicants.ApplicantCollection(
            applicant_dicts=self._mentor_dicts,
            applicant_constructor=self._get_applicant_constructor('mentor'),
        )

    @lru_cache
    def get_collection_mentees(self) -> ApplicantCollection:
        return ApplicantCollection(
            applicant_dicts=self._mentee_dicts,
            applicant_constructor=self._get_applicant_constructor('mentee'),
        )

    def get_preferredmatcher(self) -> BaseMatcher:
        with self._set_matching_type('preferred'):
            return self._get_matcher()

    def get_randommatcher(self) -> BaseMatcher:
        with self._set_matching_type('random'):
            return self._get_matcher()

    def _get_matcher(self) -> BaseMatcher:
        if self._matching_type == 'preferred':
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

    def _get_potential_pair_generator(self) -> PairsInitializer:
        if self._matching_type == 'preferred':
            pairs_builder_constructors = PreferredPairsInitializer
        elif self._matching_type == 'random':
            pairs_builder_constructors = RandomPairsInitializer
        else:
            raise ValueError
        return pairs_builder_constructors(
            mentor_dicts=self._mentor_dicts,
            pair_constructor=self._get_pair_constructor()
        )

    @staticmethod
    def _get_applicant_constructor(applicant_type: str) -> Type[ApplicantBase]:
        if applicant_type == 'mentor':
            return Mentor
        elif applicant_type == 'mentee':
            return Mentee
        else:
            raise ValueError

    def _get_pair_constructor(self) -> Type[Pair]:
        if self._matching_type == 'preferred':
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
