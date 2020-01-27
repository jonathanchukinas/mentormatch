from mentormatch.api.applicant import Mentee
from mentormatch.api.sorter.sorter_implementation import SorterHash


def test_mentee(mentees):
    mentee_dict = mentees[0]
    mentee = Mentee(
        sorter=SorterHash(),
        applicant_dict=mentee_dict,
    )
    print(repr(mentee))
    print(hash(mentee))
    assert mentee.is_available
    for _ in mentee.yield_pairs:
        assert False
    assert True
