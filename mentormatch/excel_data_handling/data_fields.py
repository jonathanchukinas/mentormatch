from bin.schema.schema import Schema
import logging


class ApplicationDataFields:

    ####################
    # MAGIC METHODS
    ####################

    def __init__(self, applicant_group):
        self.__applicant_group = applicant_group
        self.__fields = Schema.get_fields(applicant_group)
        self.__cur_index = 0  # For iterating over the fields

    def get_fields(self):
        return self.__fields

    ####################
    # INSTANCE METHODS
    ####################

    def log_missing_and_unused_fields(self, worksheet_):
        stuff = {'missing fields': self.__get_missing_fields(self.__fields),
                 'unused fields': self.__get_unused_fields(worksheet_)}
        for kind_of_fields, fields in stuff.items():
            logging.info(f'Checking `{self.__applicant_group}` worksheet for {kind_of_fields} ...')
            if len(fields) == 0:
                logging.info(f'No {kind_of_fields} found. Nice job!\n')
            else:
                logging.warning(f'Found these {kind_of_fields}: {fields}\n')

    ####################
    # STATIC METHODS
    ####################

    @staticmethod
    def __get_missing_fields(fields):
        missing_fields = []
        for field in fields:
            if field.was_found_missing():
                missing_fields.append(field.get_name())
        return sorted(missing_fields)

    @staticmethod
    def __get_unused_fields(worksheet_):
        unused_fields = set()
        for row in worksheet_:
            unused_fields.update(row.keys())
        return sorted(unused_fields)


if __name__ == '__main__':
    df_ = ApplicationDataFields('mentors')
    for field_ in df_:
        print(field_)
        print(field_.validate_value('hello'))
