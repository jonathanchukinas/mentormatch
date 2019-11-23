# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
# None


# --- Common Variables --------------------------------------------------------
groups = 'db mentees'.split()


# --- Customr Exceptions ------------------------------------------------------
class MentormatchError(Exception):
    pass


class MissingHeaderError(MentormatchError):
    pass


class UninitializedError(MentormatchError):
    pass
