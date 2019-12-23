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
from mentormatch.schema import better_match, compatible, set_current_mentor
from mentormatch.schema.fieldschema import locations, genders, fieldschemas


_pref_suffix = "yes maybe no".split()
_pref_attr = ['preference_' + val for val in _pref_suffix]


class SingleApplicant:

    group = None

    def __init__(self, db_table, doc_id, all_applicants):
        self.doc_id = doc_id
        self._all_applicants = all_applicants
        self._db_table = db_table
        hashable_string = (
                str(self.wwid) #+
                # str(self.worksheet.year)  # TODO add this back in?
        ).encode()
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
        yield from _pref_attr

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
        self._mentees = []

    def assign_mentee(self, mentee):
        mentee.matched = True
        rejected_mentee = None

        if compatible(self, mentee, mentor_only=True):
            self._mentees.append(mentee)
        else:
            rejected_mentee = mentee

        if len(self._mentees) > self.max_mentee_count:
            with set_current_mentor(self):
                sorted_mentees = sorted(self._mentees, reverse=True)
            rejected_mentee = sorted_mentees.pop()

        if rejected_mentee is not None:
            rejected_mentee.matched = False
            self._all_applicants.mentees.queue.append(rejected_mentee)

    @property
    def mentees_str(self):
        return [str(mentee) for mentee in self._mentees]

    def keys(self):
        yield from super().keys()
        yield 'mentees_str'


NoMoreMentors = sentinel.NoMoreMentors


class Mentee(SingleApplicant):

    group = "mentees"

    def __init__(self, db_table, doc_id, all_applicants):
        super().__init__(db_table, doc_id, all_applicants)
        self.preferred_mentors = self.gen_preferred_mentors()
        self.restart_count = 0
        self.matched = False  # modified by Mentor.assign_mentee()

    def gen_preferred_mentors(self):
        # Generator function for lazily looping through preferred mentors
        for wwid in self.preferred_wwids:
            mentor = self._all_applicants.mentors[wwid]
            if mentor is None:
                continue
            yield mentor
        while True:
            yield NoMoreMentors

    def assign_to_preferred_mentor(self):
        mentor = next(self.preferred_mentors)
        if mentor is not NoMoreMentors:
            # Assign to this mentor.
            mentor.assign_mentee(self)
            # The mentor may reject this match, in which case...
            # the mentee will be put back in the queue, ready to match with her next preferred mentor.
        elif self.favor and self.restart_count < 6:  # (and, implicitly, NoMoreMentors)
            # The preferred_mentors generator ran out of mentors
            # This is a "favored" mentee (meaning we *really* want her paired).
            # Therefore, restart her preferred mentors queue.
            # The next time through the process, she'll now have a slight edge over everyone else.
            self.restart_count += 1
            self.preferred_mentors = self.gen_preferred_mentors()
            self._all_applicants.mentees.queue.append(self)
        else:
            # This mentee has run out of changes to match with a preferred mentor.
            # Better luck in the random matching!
            pass

    def keys(self):
        yield from super().keys()
        yield 'favor'

    # TODO remove all these:
    def __gt__(self, other):
        if self is better_match(self, other):
            return True
        else:
            return False

    def __lt__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __ge__(self, other):
        return self.__gt__(other)

    def __le__(self, other):
        return not self.__gt__(other)




FieldResponse = collections.namedtuple("FieldResponse", "fieldname response")


class Preference:

    def __init__(self, applicant: SingleApplicant, yesmaybeno_fieldnames, selffield=None):
        self.applicant = applicant
        self.fields = yesmaybeno_fieldnames
        if selffield is not None:
            # e.g. location: This should be this person's own location
            self.self = selffield

    @property
    def yes(self):
        return self._responses("yes")

    @property
    def maybe(self):
        return self._responses("maybe")

    @property
    def any(self):
        return self._responses("yes maybe")

    def _responses(self, desired_response: str):
        responses = []
        for fieldname in self.fields:
            response = self.applicant[fieldname]
            if response in desired_response:
                responses.append(FieldResponse(fieldname, response))
