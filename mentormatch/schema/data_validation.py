import re

class DataTypeValidation:

    @staticmethod
    def get_integer(value):
        new_value = int()
        try:
            new_value = int(value)
        finally:
            return new_value

    @staticmethod
    def get_float(value):
        new_value = float()
        try:
            new_value = float(value)
        finally:
            return new_value

    @staticmethod
    def get_string(value):
        new_value = str()
        try:
            new_value = str(value).strip()
        finally:
            return new_value

    @staticmethod
    def get_boolean(value):
        new_value = bool()
        try:
            new_value = bool(value)
        finally:
            return new_value

    @classmethod
    def get_list_of_ints(cls, value):
        raw_data_as_string = cls.get_string(value)
        p = re.compile(r'\d+')  # Regular Expression for consecutive digits
        list_of_consecutive_digits = p.findall(raw_data_as_string)
        list_of_ints_ = [int(item) for item in list_of_consecutive_digits]
        return list_of_ints_

    @classmethod
    def get_first_digit(cls, value, min_integer=2, max_integer=6):
        first_integer = 0  # default value
        raw_data_as_string = cls.get_string(value)
        pattern = f'[{min_integer}-{max_integer}]'
        p = re.compile(pattern)  # Regular Expression for individual digits
        list_of_individual_digits = p.findall(raw_data_as_string)
        if 0 < len(list_of_individual_digits):
            first_digit = list_of_individual_digits[0]
            first_integer = int(first_digit)
        return first_integer

    @classmethod
    def get_list_of_str_csv(cls, value):
        raw_data_as_string = cls.get_string(value)
        list_of_words = raw_data_as_string.split(',')
        list_of_words = [word.strip() for word in list_of_words]
        return list_of_words

    @classmethod
    def get_list_of_str(cls, value):
        raw_data_as_string = cls.get_string(value)
        p = re.compile(r'\w+')  # Regular Expression for consecutive digits
        list_of_words = p.findall(raw_data_as_string)
        return list_of_words


    # TODO make sure to add a check in the wwid assignment
    #   this should log each conflict


if __name__ == '__main__':
    s = '    jonathan , nick, james  '
    print(DataTypeValidation.get_list_of_str_csv(s))