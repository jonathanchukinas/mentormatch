from mentormatch.api import main
from mentormatch.exporter import ExporterFactory


def test_main(mentors, mentees):
    pairs_summary = main(mentors, mentees)
    assert pairs_summary


def test_with_randomly_generated_applicants(lots_of_applicants, results_dir):
    # mentors = mentor_generator(1)
    # # mentees = mentee_generator(1)
    # pairs_summary = main(
    #     mentor_dicts=mentors,
    #     mentee_dicts=mentees,
    # )
    mentors = lots_of_applicants['mentors']
    mentees = lots_of_applicants['mentees']
    results = main(
        mentors,
        mentees,
    )
    print(
        '\n',
        '\nMentor Count:', len(mentors),
        '\nMentee Count:', len(mentees),
    )

    exporter = ExporterFactory(results_dir).get_exporter()
    exporter.export_inputs(mentors, mentees)
    exporter.export_results(results=results)
