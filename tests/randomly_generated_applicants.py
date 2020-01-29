import names  # TODO make sure this is added to the requires list
from random import random, randrange, choices, choice
import pytest
# TODO make sure this is in 'requirements'
import toml
from pathlib import Path
fieldschema_path = Path(__file__).parent.parent / 'api' / 'app' / 'fieldschema.toml'
fieldschema = toml.load(fieldschema_path)


def randomly_generated_mentors(mentor_count=1):
    mentors = []
    for _ in range(mentor_count):
        mentor = {
            'max_mentee_count': 1,
        }
        mentor.update(random_person())
        mentor['function'] = ['being awesome']
        mentor['position_level'] = 3
        mentor['years_total'] = 20
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
        mentee['function'] = ['being awesome']
        mentee['position_level'] = 3
        mentee['years_total'] = 20
        mentees.append(mentee)
    return mentees





@pytest.fixture(scope='function')
def random_person():

    _dict = {
        'last_name': names.get_last_name(),
        'wwid': randrange(1, 1000),
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
