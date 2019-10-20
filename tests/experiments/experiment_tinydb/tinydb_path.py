"""
What I learned:
If I want to delete the json file, there can't still be a db object in memory.
So either:
1) del the db
2) use with
"""


from pathlib import Path
from tinydb import TinyDB


def start_db(path):
    return TinyDB(path)


def end_db(path):
    path.unlink()


def do_stuff(db):
    bob = {
        'name': 'bob',
        'wwid': 123
    }
    db.insert(bob)


db_path = Path.home() / '.mentormatch.json'
with start_db(db_path) as mm_db:
    do_stuff(mm_db)
    print(mm_db)
# del mm_db
end_db(db_path)


