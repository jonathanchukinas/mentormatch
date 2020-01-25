from mentormatch.utils.enums import ApplicantType


def test_enum_applicant_type():
    mentor: ApplicantType = ApplicantType.MENTOR
    mentee: ApplicantType = ApplicantType.MENTEE
    assert mentor is ApplicantType.MENTOR
    assert mentee is ApplicantType.MENTEE
    assert mentor == ApplicantType.MENTOR
    assert mentee == ApplicantType.MENTEE
    assert mentor.get_other() is ApplicantType.MENTEE
    assert mentee.get_other() is ApplicantType.MENTOR
