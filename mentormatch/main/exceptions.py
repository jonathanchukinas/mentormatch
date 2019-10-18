# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


class MentormatchError(Exception):
    pass


class MissingHeaderError(MentormatchError):
    pass


class UninitializedError(MentormatchError):
    pass
