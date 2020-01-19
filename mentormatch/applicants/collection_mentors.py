class CollectionMentors(GroupApplicants):

    def __init__(self, mentor_dicts):
        self.groupname = 'mentors'
        super().__init__(db, all_applicants, Mentor)

    # def __getitem__(self, wwid) -> Mentor:
    #     return self._group_applicants.get(wwid, None)


if __name__ == '__main__':
    pass
