from mentormatch.applicants import SingleApplicant


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