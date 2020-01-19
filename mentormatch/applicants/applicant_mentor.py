from mentormatch.applicants import SingleApplicant


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