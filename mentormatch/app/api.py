from mentormatch.configuration import configuration


def main(path=None):

    path_getter = configuration.get_pathgetter()
    path_getter.get_path()

    applications_importer = configuration.get_importer()
    applications_importer.import_mentor_dicts()
    applications_importer.import_mentee_dicts()

    mentors = configuration.get_collection_mentors()
    mentees = configuration.get_collection_mentees()
    


    # --- Path to excel workbook ----------------------------------------------
    path = selectfile.get_path() if path is None else path

    # --- get applications, build applicants ----------------------------------
    try:
        applicants = AllApplicants(path)
    except exceptions.MentormatchError as e:
        click.echo(e)
        return

    # --- preferred matching --------------------------------------------------
    matching_algorithm = Matching(applicants)
    matching_algorithm.preferred_matching()
    matching_algorithm.random_matching()

    # --- print results -------------------------------------------------------
    applicants.write_to_toml()


if __name__ == "__main__":
    pass
