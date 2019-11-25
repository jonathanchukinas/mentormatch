""""""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import datetime

# --- Third Party Imports -----------------------------------------------------
from tinydb import TinyDB, Query

# --- Intra-Package Imports ---------------------------------------------------
# None


def get_clean_db(path=None, year=None) -> TinyDB:
    path = Path.home() / ".mentormatch.json" if path is None else path
    db = TinyDB(path)
    db.purge()   # TODO or purge_tables() ?
    db.year = datetime.datetime.now().year if year is None else year
    return db


def add_group_to_db(group_name, records, database, autosetup=False):
    db_table = database.table(group_name)
    db_table.insert_multiple(records)
    # TODO why did I do "autosetup"?
    # if autosetup:
    #     drop_dups(db_table)


def drop_dups(db_table):
    """If any wwid is duplicated, keep only the most recent."""
    db_table: TinyDB
    applicant = Query()
    dup_ids = set()
    for record in db_table:
        wwid = record.wwid

        # TODO
        #   Count applicants that match that wwid
        #   if count ==1, continue
        #   else: find the one with the most recent date
        #   collect all ids
    db_table.remove(doc_ids=dup_ids)
    # TODO
    #   add field for application date
