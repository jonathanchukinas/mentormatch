""""""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import datetime

# --- Third Party Imports -----------------------------------------------------
from tinydb import TinyDB, Query

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch.excel import selectfile


def get_clean_db(path=None, year=datetime.datetime.now().year):
    if path is None:
        path = Path.home() / ".mentormatch.json"
    db = TinyDB(path)
    db.purge()   # TODO or purge_tables() ?
    db.year = year
    return db


def import_worksheet_to_db(
    workbook,
    excel_sheet_name,
    database: TinyDB,
    group=None,  # Will be set equal to excel_sheet_name
    header=None,
    field_validation=None,
    autosetup=False,
):
    # --- get worksheet -------------------------------------------------------
    ws = selectfile.get_worksheet(workbook, excel_sheet_name)

    # --- header logic --------------------------------------------------------
    if header is None:
        header_names = None
        header_row = 1
    elif isinstance(header, int):
        header_names = None
        header_row = header
    elif isinstance(header, list):
        header_names = header
        header_row = selectfile.get_header_row_number(ws, header_names)
    else:
        msg = "This function accepts only None, int, and list as args for header parameter"
        raise ValueError(msg)
    if header_names is None:
        header_names = selectfile.get_header_names(ws, header_row)

    # --- get dict for each row -----------------------------------------------
    records = selectfile.convert_rows_to_dicts(ws, header_row, header_names)

    # --- db ------------------------------------------------------------------
    if group is None:
        group = excel_sheet_name
    db_table = database.table(group)
    db_table.insert_multiple(records)

    # --- validate data -------------------------------------------------------
    if field_validation:
        validate_fields(db_table, field_validation)

    # --- autosetup, in applicable --------------------------------------------
    if autosetup:
        drop_dups(db_table)

    # --- return --------------------------------------------------------------
    return db_table


def validate_fields(db: TinyDB, field_validation):
    for applicant in db:
        for field in field_validation:
            val_func = field.val_func



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
