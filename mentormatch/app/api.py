from mentormatch.configuration.configuration import Factory


def main():

    factory = Factory()

    factory.get_pathgetter().get_path()

    applications_importer = factory.get_importer()
    applications_importer.import_mentor_dicts()
    applications_importer.import_mentee_dicts()

    factory.get_collection_mentors().build_applicant_objects()
    factory.get_collection_mentees().build_applicant_objects()

    factory.get_preferredmatcher().run()
    factory.get_randommatcher().run()

    factory.get_exporter().export()


if __name__ == "__main__":
    main()
