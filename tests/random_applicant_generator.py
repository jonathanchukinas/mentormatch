from __future__ import annotations
import names  # TODO make sure this is added to the requires list-
from random import random, randrange, choices, choice
import pytest
# TODO make sure this is in 'requirements'
import toml
from pathlib import Path
from collections import namedtuple

# For Typing:
from typing import Dict, List


class RandomApplicantGenerator:

    def __init__(self):
        self.mentor_dicts = []
        self.mentee_dicts = []
        fieldschema_path = Path(__file__).parent.parent / 'mentormatch' / 'api' / 'app' / 'fieldschema.toml'
        self._fieldschema = toml.load(fieldschema_path)
        self.applicants_dicts = {
            'mentors': self.mentor_dicts,
            'mentees': self.mentee_dicts,
        }

    def build_mentors(self, mentor_count: int) -> None:
        first_wwid = len(self.mentor_dicts) + 1
        last_wwid = first_wwid + mentor_count
        for wwid in range(first_wwid, last_wwid):
            self.mentor_dicts.append(self._build_random_mentor())

    def build_mentees(self, mentee_count: int) -> None:
        first_wwid = len(self.mentee_dicts) + 1
        last_wwid = first_wwid + mentee_count
        for wwid in range(first_wwid, last_wwid):
            self.mentee_dicts.append(self._build_random_mentee())

    def _get_mentor_wwids(self) -> List[int]:
        return [
            mentor_dict['wwid']
            for mentor_dict in self.mentor_dicts
        ]

    def _build_random_mentor(self, wwid=None):
        mentor = {
            'max_mentee_count': self._rand_max_mentee_count(),
        }
        mentor.update(self._build_applicant_dict())
        mentor.update(self._build_experience_dict('mentor'))
        if wwid is not None:
            mentor['wwid'] = wwid
        return mentor

    @staticmethod
    def _rand_max_mentee_count():
        return choices(
            population=[1, 2, 3],
            weights=[75, 20, 5],
            k=1,
        )[0]

    def _build_random_mentee(self, wwid=None):
        mentee = {
            'favor': self._rand_favor(),
            'preferred_functions': self._get_preferred_functions(),
            'preferred_wwids': self._get_preferred_wwids(),
        }
        mentee.update(self._build_applicant_dict())
        mentee.update(self._build_experience_dict('mentee'))
        if wwid is not None:
            mentee['wwid'] = wwid
        return mentee

    @staticmethod
    def _rand_favor():
        return choices(
            population=[0, 1, 2, 3],
            weights=[400, 20, 10, 1],
            k=1
        )[0]

    def _get_preferred_functions(self) -> List[str]:
        return choices(
            population=self._fieldschema['selections']['locations'],
            k=randrange(0, 7),
        )

    def _build_applicant_dict(self):

        _dict = {
            'last_name': names.get_last_name(),
            'wwid': randrange(1, 1000),
            'function': choice(self._fieldschema['selections']['function'])
        }

        # Yes / No / Maybe
        yesnomaybe = [
            'preference_' + suffix
            for suffix in 'yes maybe no'.split()
        ]
        _dict.update({
            key: []
            for key in yesnomaybe
        })

        # Gender-related keys
        genders = 'male female'.split()
        gender_self = choice(genders)
        _dict['gender'] = gender_self
        _dict['first_name'] = names.get_first_name(gender_self)
        _dict['preference_yes'].append('female')
        preference_for_male = choices(yesnomaybe, [0.8, 0.1, 0.1], k=1)[0]
        _dict[preference_for_male].append('male')

        # Locations
        locations = self._fieldschema['selections']['locations']
        location_count = len(locations)
        _dict['location'] = choice(locations)
        location_preferences = choices(yesnomaybe, [0.8, 0.1, 0.1], k=location_count)
        for location, location_preference in zip(locations, location_preferences):
            _dict[location_preference].append(location)

        # Skills
        skill_count = randrange(0, 5)
        _dict['skills'] = [
            choice(self._fieldschema['selections']['skills'])
            for _ in range(skill_count)
        ]

        return _dict

    @staticmethod
    def _build_experience_dict(applicant_type) -> Dict:
        LevelParams = namedtuple('LevelParams', 'years_min years_max')
        position_level_weights = {
            'mentor': {
                2: 0.1,
                3: 0.3,
                4: 0.3,
                5: 0.2,
                6: 0.1,
            },
            'mentee': {
                2: 0.5,
                3: 0.3,
                4: 0.1,
                5: 0.1,
                # 6: 0.0,  # TODO how many levels are there?
            },
        }
        years_prob = {
            2: LevelParams(1, 20),
            3: LevelParams(10, 30),
            4: LevelParams(20, 40),
            5: LevelParams(25, 50),
            6: LevelParams(30, 50),
        }

        level_prob = position_level_weights[applicant_type]
        levels = list(level_prob.keys())
        prob = list(level_prob.values())

        level = choices(levels, prob, k=1)[0]
        years = randrange(
            start=years_prob[level].years_min,
            stop=years_prob[level].years_max
        )

        return {
            'years_total': years,
            'position_level': level,
        }

    def _get_preferred_wwids(self) -> List[int]:
        mentor_wwids = self._get_mentor_wwids()
        if len(mentor_wwids) == 0:
            return []
        preferred_wwid_count_probability = {
            10: .05,
            9: .06,
            8: .07,
            7: .08,
            6: .1,
            5: .15,
            4: .2,
            3: .4,
            2: .45,
            1: .5,
            0: 1,
        }
        pref_wwid_count = choices(
            population=list(preferred_wwid_count_probability.keys()),
            cum_weights=list(preferred_wwid_count_probability.values()),
            k=1,
        )[0]
        return list(set(choices(mentor_wwids, k=pref_wwid_count)))
