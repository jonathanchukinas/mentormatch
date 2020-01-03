# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Custom Exceptions ------------------------------------------------------
class MentormatchError(Exception):
    pass


class UninitializedError(MentormatchError):
    pass


# Note: the following two exceptions ensure that fieldschema.py and fieldschema.toml align with each other.
class MissingFieldschemaError(MentormatchError):
    def __init__(self, tablename, fieldname):  # TODO make sure this gets used
        message = f"Error: In fieldschema.toml, the {repr(fieldname)} " \
                  f"field is missing from the {repr(tablename)} table."
        super().__init__(message)


class UnusedFieldschemaError(MentormatchError):  # TODO make sure this gets used
    def __init__(self, tablename, fieldnames):
        message = f"Error: fieldschema.toml contains the fields {repr(fieldnames)} " \
                  f"in the {repr(tablename)} table that aren't used by the mentormatch algorithm."
        super().__init__(message)
