from tinydb import TinyDB, Query, where

db = TinyDB('db.json')
db.purge()
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
db.insert_multiple(mentor_list)
applicants = db.all()
# print(applicants)
print(type(applicants))  # list
for applicant in applicants:
    print(type(applicant))  # tinydb.database.Document
    applicant.last_name = 'Lincoln'  # This doesn't do anything.
    applicant['wwid'] = 1  # need to use dictionary notation
    db.write_back([applicant])  # Either this or the next line works fine. Note that applicant is in a list
# db.write_back(applicants)
for applicant in db:
    print(applicant)
