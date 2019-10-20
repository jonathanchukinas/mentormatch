""""""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import datetime

# --- Third Party Imports -----------------------------------------------------
from tinydb import TinyDB

# --- Intra-Package Imports ---------------------------------------------------
# None


def get_clean_db(path=None):
    if path is None:
        path = Path.home() / '.mentormatch.json'
    db = TinyDB(path)
    db.purge_tables()
    return db


def import_worksheet_to_db(
    workbook,
    excel_sheet_name,
    database,
    header_row=1,
    find_header_row=False,
    autosetup=False,
    group=None,
    year=datetime.datetime.now().year,
):
    






