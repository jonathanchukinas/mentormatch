import names  # TODO make sure this is added to the requires list
from random import random, randrange, choices, choice
import pytest
# TODO make sure this is in 'requirements'
import toml
from pathlib import Path
fieldschema_path = Path(__file__).parent.parent / 'mentormatch' / 'api' / 'app' / 'fieldschema.toml'
fieldschema = toml.load(fieldschema_path)


def randomly_generated_mentors(mentor_count=1):
    mentors = []
    for _ in range(mentor_count):
        mentor = {
            'max_mentee_count': randrange(2, 5),
        }
        mentor.update(random_person())
        mentor.update(get_experience('mentor'))
        mentors.append(mentor)
    return mentors


def randomly_generated_mentees(mentor_count=1):
    mentees = []
    for _ in range(mentor_count):
        mentee = {
            'favor': 1,
            'preferred_functions': [],
            'preferred_wwids': [],
        }
        mentee.update(random_person())
        mentee['position_level'] = 3
        mentee['years_total'] = 20
        mentee.update(get_experience('mentee'))
        mentees.append(mentee)
    return mentees


def random_person():

    _dict = {
        'last_name': names.get_last_name(),
        'wwid': randrange(1, 1000),
        'function': choice(fieldschema['selections']['function'])
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
    locations = fieldschema['selections']['locations']
    location_count = len(locations)
    _dict['location'] = choice(locations)
    location_preferences = choices(yesnomaybe, [0.8, 0.1, 0.1], k=location_count)
    for location, location_preference in zip(locations, location_preferences):
        _dict[location_preference].append(location)

    # Skills
    skill_count = randrange(0, 5)
    _dict['skills'] = [
        choice(fieldschema['selections']['skills'])
        for _ in range(skill_count)
    ]

    return _dict


def get_experience(applicant_type):
    if applicant_type == 'mentor':
        level_prob = {
            2: 0.1,
            3: 0.3,
            4: 0.3,
            5: 0.2,
            6: 0.1,
        }
    else:
        level_prob = {
            2: 0.5,
            3: 0.3,
            4: 0.1,
            5: 0.1,
            # 6: 0.0,  # TODO how many levels are there?
        }
    levels = level_prob.keys()
    prob = level_prob.values()
    level = choices(levels, prob)
    return {
        'years_total': 1,  # TODO
        'position_level': level,
    }
