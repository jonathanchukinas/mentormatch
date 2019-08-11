# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


class MentormatchError(Exception):
    pass


class MentormatchFileError(MentormatchError):
    """
    Raise this for any errors related to the excel file itself.
    Examples:
        wrong file extension
        file missing
        missing worksheet
    """
    pass


class UninitializedError(Exception):
    pass


class Uninitialized(MentormatchError):
    pass
