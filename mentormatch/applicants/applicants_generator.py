from bin.excel_data_handling.excel_data_handler import ExcelDataHandler
from bin.applicants.applicants_group import ApplicantsGroup
from bin.schema.schema import Schema


class ApplicantsGenerator:

    def __init__(self, applicant_data):
        self.__ready = False
        if applicant_data:
            self.__applicant_data = applicant_data
            self.__ready = True

    def generate_applicants(self):
        if self.__ready:
            # Convert Excel Data to Objects
            applicants = dict()
            for group in Schema.applicant_groups:
                applicants[group] = ApplicantsGroup(self.__applicant_data[group], group)
                # TODO
                #   Quality check on mentor/ee containers.
                #       Sites names and counts
                #       Gender names and counts
                #       Number of mentors and mentees
        else:
            return False
            # TODO should return None instead
