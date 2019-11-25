"""The Applicant object represents a single applicant. It stores very little
data on its own. It has access to a Worksheet object"""

# --- Standard Library Imports ------------------------------------------------
import hashlib
from unittest.mock import sentinel  # https://www.revsys.com/tidbits/sentinel-values-python/

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.applicants.match_quality import compatible


class SingleApplicant:

    group = None

    def __init__(self, db, doc_id, all_applicants):
        self.doc_id = doc_id
        self._all_applicants = all_applicants
        self._db_table = db  # TODO is this the whole db or just a table? I'll assume it's a table for now
        hashable_string = (str(self.wwid) + str(self.worksheet.year)).encode()
        self.hash = hashlib.sha1(hashable_string)  # Used for semi-random sorting

    def __eq__(self, other):
        # Also used to makes sure a mentee doesn't get matched with herself.
        return self.wwid == other.wwid

    def __str__(self):
        name = ' '.join([self.first_name, self.last_name]).strip()
        return f'WWID: {self.wwid}\t Name: {name}'

    def __getattr__(self, attribute_name):
        db = self._db_table
        record = db.get(doc_id=self.doc_id)
        return record[attribute_name]





class Mentor(SingleApplicant):

    group = "mentors"

    def __init__(self, db, doc_id, all_applicants):
        super().__init__(db, doc_id, all_applicants)
        self._mentees = []

    def assign_mentee(self, mentee):
        rejected_mentee = None
        if compatible(self, mentee):
            self._mentees.append(mentee)
            # TODO sort by **DECREASING** match quality
        else:
            rejected_mentee = mentee
        if len(self._mentees) > self.max_mentee_count:
            rejected_mentee = self._mentees.pop()
        if rejected_mentee is not None:
            self._all_applicants.mentees.queue.append(rejected_mentee)


NoMoreMentors = sentinel.NoMoreMentors


class Mentee(SingleApplicant):

    group = "mentees"

    def __init__(self, db, doc_id, all_applicants):
        super().__init__(db, doc_id, all_applicants)
        self.preferred_mentors = self.gen_preferred_mentors()
        self._restart_count = 0

    def gen_preferred_mentors(self):
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
        elif self.favored and self._restart_count < 6:  # (and, implicitly, NoMoreMentors)
            # The preferred_mentors generator ran out of mentors
            # This is a "favored" mentee (meaning we *really* want her paired).
            # Therefore, restart her preferred mentors queue.
            # The next time through the process, she'll now have a slight edge over everyone else.
            self._restart_count += 1
            self.preferred_mentors = self.gen_preferred_mentors()
            self._all_applicants.mentees.queue.append(self)
        else:
            # This mentee has run out of changes to match with a mentor.
            # Better luck in the random matching!
            pass
