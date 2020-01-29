from mentormatch.api import main


def test_main(mentors, mentees):
    pairs_summary = main(mentors, mentees)
    assert True


def test_with_randomly_generated_applicants(lots_of_applicants):
    # mentors = mentor_generator(1)
    # # mentees = mentee_generator(1)
    # pairs_summary = main(
    #     mentor_dicts=mentors,
    #     mentee_dicts=mentees,
    # )
    pairs_summary = main(
        lots_of_applicants['mentors'],
        lots_of_applicants['mentees'],
    )
    assert True
