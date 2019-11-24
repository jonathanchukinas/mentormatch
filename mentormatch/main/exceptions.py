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
