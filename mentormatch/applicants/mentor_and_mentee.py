"""The Applicant object represents a single applicant. It stores very little
data on its own. Calls to its attributes trigger database calls."""

# --- Standard Library Imports ------------------------------------------------
import hashlib
from unittest.mock import sentinel  # https://www.revsys.com/tidbits/sentinel-values-python/
import collections
import reprlib

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# from mentormatch.schema import better_match, compatible, set_current_mentor # TODO remove?
from mentormatch.schema.fieldschema import locations, genders, fieldschemas


_pref_suffix = "yes maybe no".split()
_pref_attr = ['preference_' + val for val in _pref_suffix]


class SingleApplicant:

    group = None

    def __init__(self, db_table, doc_id, all_applicants):
        self.doc_id = doc_id
        self.applicants = all_applicants
        self._db_table = db_table
        hashable_string = (str(self.wwid)).encode()
        self.hash = hashlib.sha1(hashable_string).hexdigest()  # Used for semi-random sorting
        # self.locations = Preference(self, locations, self.site)
        # self.genders = Preference(self, genders, self.gender)
        for pref_suffix, pref_attr in zip(_pref_suffix, _pref_attr):
            setattr(self, pref_attr, self._preferences(pref_suffix))
        self.name = ' '.join([self.first_name, self.last_name]).strip()
        self.preference_self = [self.location, self.gender]

    def __eq__(self, other):
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.wwid == other.wwid

    def __str__(self):
        return f'{self.wwid} {self.name}'

    # @property
    # def name(self):
    #     return ' '.join([self.first_name, self.last_name]).strip()

    def __getattr__(self, attribute_name):
        db = self._db_table
        record = db.get(doc_id=self.doc_id)
        return record[attribute_name]

    def __repr__(self):
        classname = self.__class__.__name__
        # personname = repr(self.name)
        obj_id = hex(id(self))
        # {str(self)}
        return f"<{classname} {str(self)} @{obj_id}>"

    def keys(self):
        yield from (
            field.name
            for field in fieldschemas[self.group]
            if field.name not in locations + genders
        )
        yield from _pref_attr  # TODO what is this?
        yield 'paired_with'  # TODO implement

    def __getitem__(self, key):
        return getattr(self, key, None)

    def _preferences(self, yes_no_or_maybe):
        if yes_no_or_maybe not in _pref_suffix:
            raise ValueError(f"yes_no_or_maybe must be one of {_pref_suffix}. You passed {yes_no_or_maybe}.")
        prefs = collections.defaultdict(list)
        for value in locations + genders:
            key = self[value]
            prefs[key].append(value)
        return prefs[yes_no_or_maybe]


class Mentor(SingleApplicant):

    group = "mentors"

    def __init__(self, db_table, doc_id, all_applicants):
        super().__init__(db_table, doc_id, all_applicants)
        self.assigned_pairs = []

    @property
    def paired_with(self):
        return [str(pair.mentee) for pair in self.assigned_pairs]

    @property
    def below_capacity(self):
        return self.mentee_count < self.max_mentee_count

    @property
    def over_capacity(self):
        return self.mentee_count > self.max_mentee_count

    @property
    def mentee_count(self):
        return len(self.assigned_pairs)


# NoMoreMentors = sentinel.NoMoreMentors  # TODO remove?


class Mentee(SingleApplicant):

    group = "mentees"

    def __init__(self, db_table, doc_id, all_applicants):
        super().__init__(db_table, doc_id, all_applicants)
        # self.preferred_mentors = self.gen_preferred_mentors()
        self.restart_count = 0
        self.assigned_pair = None

    def keys(self):
        yield from super().keys()
        yield 'favor'

    @property
    def paired_with(self):
        if self.paired:
            return str(self.assigned_pair.mentor)
        else:
            return '...unpaired...'

    @property
    def paired(self):
        return self.assigned_pair is not None

    @property
    def favored(self):
        return self.favor > 0

    @property
    def selected_preferred_mentors(self) -> bool:
        # TODO rename to something better ... 'wanted_pref_mentors'?...
        return len(self.preferred_wwids) > 0
