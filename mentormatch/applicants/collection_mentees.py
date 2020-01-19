from mentormatch.applicants.collection_mentors import GroupApplicants


class CollectionMentees(GroupApplicants):

    def __init__(self, mentee_dicts):
        self.groupname = 'mentees'
        super().__init__(db, all_applicants, Mentee)
        self.queue = None  # add right, pop left

    # def awaiting_preferred_mentor(self) -> Mentee:
    #     if self.queue is None:
    #         randomly_sorted_mentees = sorted(self._group_applicants.values(), key=lambda mentee: mentee.hash)
    #         self.queue = collections.deque(randomly_sorted_mentees)
    #     while len(self.queue) > 0:
    #         next_mentee = self.queue.popleft()
    #         yield next_mentee
    #     return