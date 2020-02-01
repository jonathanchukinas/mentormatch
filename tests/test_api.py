from mentormatch.api import main


def test_main(mentors, mentees):
    pairs_summary = main(mentors, mentees)
    assert pairs_summary


def test_with_randomly_generated_applicants(lots_of_applicants):
    # mentors = mentor_generator(1)
    # # mentees = mentee_generator(1)
    # pairs_summary = main(
    #     mentor_dicts=mentors,
    #     mentee_dicts=mentees,
    # )
    mentors = lots_of_applicants['mentors']
    mentees = lots_of_applicants['mentees']
    pairs_summary = main(
        mentors,
        mentees,
    )
    assert pairs_summary
    print(len(pairs_summary))
