# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Common Variables --------------------------------------------------------
groups = 'db mentees'.split()


# --- Custom Exceptions ------------------------------------------------------
class MentormatchError(Exception):
    pass


class UninitializedError(MentormatchError):
    pass
