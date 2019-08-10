def wrap_applicant_for_matching(applicant):
    applicant_group = applicant.applicant_group
    wrappers = {'mentors': MentorWrapper,
                'mentees': MenteeWrapper}
    wrapper = wrappers[applicant_group]
    return wrapper(applicant)


class ApplicantWrapper:

    def __init__(self, applicant):
        self.applicant = applicant
        self.data = applicant.application

    def get_hash(self):
        # import hashlib
        #
        # my_name = 'jonathan chukinas' + str(2019)
        # my_name = my_name.encode('utf-8')
        # # my_name = b'jonathan chukinas 2019'
        # print(my_name)
        #
        # hash_object = hashlib.sha1(my_name)
        # hex_dig = hash_object.hexdigest()
        # print(hex_dig)
        #
        # bros = ['jonathan', 'nicholas', 'austin', 'james']
        # bros = [name.encode('utf-8') for name in bros]
        # print(bros)
        # bros_hash = [hashlib.sha1(name).hexdigest() for name in bros]
        #
        # print(bros_hash)
        # print(sorted(bros_hash))
        pass


class MentorWrapper(ApplicantWrapper):

    def __init__(self, applicant):
        super().__init__(applicant)
        self.__tentative_mentees = []
        self.__committed_mentees = []

    def add_mentee(self, mentee):
        self.__tentative_mentees.append(mentee)
        ##
        #
        #
        return None # or the rejected mentee


class MenteeWrapper(ApplicantWrapper):

    def __init__(self, applicant):
        super().__init__(applicant)
        self.__matched = False
        self.__rejection_count = 0

    def still_unmatched(self):
        return self.__matched

    def mark_as_matched(self):
        self.__matched = True

    def could_not_find_a_match(self):
        self.__rejection_count += 1
        # TODO adjust the "priority" tie breaker to be more favorable for this mentee.

    def still_has_chances(self):
        if self.__rejection_count < 6
