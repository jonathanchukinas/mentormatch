"""The ApplicantBase object represents a single applicant. It stores very little
data on its own. Calls to its attributes trigger database calls."""

import hashlib
import collections
from mentormatch.configuration.fieldschema import locations, genders, fieldschemas


_pref_suffix = "yes maybe no".split()
_pref_attr = ['preference_' + val for val in _pref_suffix]


class ApplicantBase:

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
        self._str = f'{self.wwid} {self.name}'

    def __eq__(self, other):
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.wwid == other.wwid

    def __str__(self):
        return self._str

    # @property
    # def name(self):
    #     return ' '.join([self.first_name, self.last_name]).strip()

    def __getattr__(self, attribute_name):
        db = self._db_table
        record = db.get(doc_id=self.doc_id)
        return record[attribute_name]

    def __repr__(self):
        classname = self.__class__.__name__  # pragma: no cover
        obj_id = hex(id(self))  # pragma: no cover
        return f"<{classname} {str(self)} @{obj_id}>"  # pragma: no cover

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
            raise ValueError(f"yes_no_or_maybe must be one of {_pref_suffix}. You passed {yes_no_or_maybe}.")  # pragma: no cover
        prefs = collections.defaultdict(list)
        for value in locations + genders:
            key = self[value]
            prefs[key].append(value)
        return prefs[yes_no_or_maybe]
