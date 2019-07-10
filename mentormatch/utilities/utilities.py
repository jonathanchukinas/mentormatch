def ensure_string(value):
    string_ = ''
    try:
        string_ = str(value)
    finally:
        return string_


def ensure_integer(value):
    integer_ = 0
    try:
        integer_ = int(value)
    finally:
        return integer_
