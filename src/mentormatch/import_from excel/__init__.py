# TODO pseudocode
#   User types `mentormatch import`
#   Check db for excel paths.
#   reuse = False
#   If exists
#       if user wants to use it
#           reuse = True
#   if reuse
#       reuse
#   else
#       user selects from dialog box
#   Check that file exists. throw error if not.
#   Check if file contains mentors and mentees. Throw error if not
#   Check each spreadsheet for its fields. For each spreadsheet:
#       throw error if a field is missing (make sure to list all the missing ones)
#       throw error if field is duplicated (list all the dups. Use a counter?)
#       throw warning if extra fields (list all extras)
#   For each field
#       check for correctness
#       use counter and report on either all or some of the values (so user can see what was entered)
#       throw errors where necessary
#       If all correct, report on random assortment with counts
#       If incorrect, show some of all of the failures. Throw an error
#   purge db tables mentors and mentees
#   add mentors and mentees to db
#   report successful add


# TODO
#   make a note in the readme that formulas are not read
#   report on number of rows and applicants in each ws
#       Note that it's an excel quirk that a once-populated row still counts as a populated row. You must delete the row
