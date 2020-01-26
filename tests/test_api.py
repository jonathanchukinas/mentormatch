from mentormatch.api import main


def test_main(mentors, mentees):
    pairs_summary = main(mentors, mentees)
    assert True
