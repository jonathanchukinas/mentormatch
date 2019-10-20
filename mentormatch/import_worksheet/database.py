""""""

# --- Standard Library Imports ------------------------------------------------
from pathlib import Path
import datetime

# --- Third Party Imports -----------------------------------------------------
from tinydb import TinyDB, Query

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
    pass


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



    if 'row' not in self.df:
        self.add_row_column()
    rows_initial = list(self.df['row'])
    self.df.drop_duplicates(subset='wwid', keep='first', inplace=True)
    rows_after = list(self.df['row'])
    rows_removed = [row for row in rows_initial if row not in rows_after]
    if rows_removed:
        click.echo("\nIf a wwid is duplicated, only the first instance is kept.")
        click.echo(f'The following rows from the {self.sheetname} workbook were ignored as a result:')
        click.echo(rows_removed)
        return rows_removed
    return []






