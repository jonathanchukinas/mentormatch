from mentormatch.api.applicant import Applicant
from mentormatch.api.sorter.sorter_implementation import SorterHash


def test_applicant_repr(mentors):
    mentor_dict = mentors[0]
    mentor = Applicant(mentor_dict, ranker=SorterHash())  # TODO rename to sorter
    print(repr(mentor))
    print(hash(mentor))
    assert True
