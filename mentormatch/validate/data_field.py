from bin.schema.data_validation import DataTypeValidation as V


class DataField:

    def __init__(self, field_name, validation_function=V.get_string, applicant_group='both'):
        """An Instance represents a single field from the applicant.
        It knows which worksheets it resides in.
        It validates the applicant from those fields.
        It stores log applicant for this field (found? bad applicant? etc)
        It will never be asked to check for applicant in a worksheet it doesn't apply to (e.g. max_mentee_count for mentees)

        :param field_name: e.g. 'first_name', 'wwid', 'sites_yes'
        :param validation_function: 'string', 'integer', 'string in int' ...
        :param applicant_group: 'mentors', 'mentees', or 'both'
        """
        self.__field_name = field_name

        self.__validation_function = validation_function

        self.__applicant_group = applicant_group
        if applicant_group not in ['mentors', 'mentees', 'both']:
            logging.debug(f'SingleDataField initialized with wrong value: {applicant_group}')

        self.__warnings = {'missing_field': False,
                           'bad_data': []}

    def __str__(self):
        if self.__applicant_group == 'both':
            group = 'mentors and mentees'
        else:
            group = self.__applicant_group
        return f'{self.__field_name}: {group}'

    def validate_field(self, unvalidated_applicant):
        """Check for field; validate its value"""
        if self.__field_name in unvalidated_applicant:
            # Removing it from dict allows us later to report on unused keys
            value = unvalidated_applicant.pop(self.__field_name)
        else:
            self.__warnings['missing_field'] = True
            value = str()

        validated_value = self.validate_value(value)
        return validated_value

    def validate_value(self, value):
        return self.__validation_function(value)

    def applicable_to(self, applicant_group):
        """

        :param applicant_group: 'mentors', 'mentees', or 'both'
        :return:
        """
        if self.__applicant_group == 'both' or self.__applicant_group == applicant_group:
            return True
        else:
            return False

    def was_found_missing(self):
        return self.__warnings['missing_field']

    def get_name(self):
        return self.__field_name
