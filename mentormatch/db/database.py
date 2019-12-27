""""""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import datetime

# --- Third Party Imports -----------------------------------------------------
from tinydb import TinyDB, Query

# --- Intra-Package Imports ---------------------------------------------------
# None


def now_str(pretty=False):
    if pretty:
        return datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    else:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def get_clean_db(path=None, year=None) -> TinyDB:
    dir = Path.home() / "mentormatch"
    dir.mkdir(exist_ok=True, parents=True)
    file_path = dir / f".mentormatch_{now_str()}.json" if path is None else path

    # TODO remove:
    # try:
    #     path.unlink()
    # except FileNotFoundError:
    #     pass
    # print(path)
    db = TinyDB(file_path)
    # db.purge_tables()
    # db.year = datetime.datetime.now().year if year is None else year  # TODO add this back in?
    return db


def add_group_to_db(group_name, records, database):
    db_table = database.table(group_name)
    db_table.insert_multiple(records)


def drop_dups(db_table):
    """If any wwid is duplicated, keep only the most recent."""
    db_table: TinyDB
    applicant = Query()
    dup_ids = set()
    for record in db_table:
        wwid = record.wwid
    db_table.remove(doc_ids=dup_ids)
