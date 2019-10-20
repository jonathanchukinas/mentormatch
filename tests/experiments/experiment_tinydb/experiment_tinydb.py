from tinydb import TinyDB, Query, where

db = TinyDB('db.json')
db.purge_tables()
mentors = db.table('mentors')
mentor_list = list()
mentor_list.append({
    'first_name': 'Jonathan',
    'last_name': 'Chukinas',
    'wwid': 1052648,
    'preferred_wwids': [132, 234, 345],
})
mentor_list.append({
    'first_name': 'Nick',
    'last_name': 'Chukinas',
    'wwid': 45673,
    'preferred_wwids': [345],
})
mentor_list.append({
    'first_name': 'Kelsey',
    'last_name': 'Ritter',
    'wwid': 123456,
    'preferred_wwids': [345, 45673],
})

mentor_ids = mentors.insert_multiple(mentor_list)
print(mentor_ids)
# mentor_element = mentors.get(eid=mentor_ids)
print(mentors)
brothers = mentors.search(where('last_name') == 'Chukinas')
print(brothers)

# --- Experiment with Query ---------------------------------------------------
applicant = Query()
brothers = mentors.get(applicant.last_name == 'Chukinas')
print(brothers)
print('element count:', len(mentors))
print(mentors)
