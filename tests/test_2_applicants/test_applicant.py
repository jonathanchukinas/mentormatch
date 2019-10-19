"""The Applicants object is a container of Applicant objects."""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import applicant as applicant_classes


def test_applicant(fixture_get_ws):
    ws = fixture_get_ws('drop_dups', autosetup=True)
    df = ws.df
    print()
    print(df)

    row = df.iloc[0]
    print()
    print(row)

    name = row['first_name']
    print()
    print(name)

    applicant = applicant_classes.Applicant(ws, 0)
    print()
    print(applicant.first_name)
    print(applicant)
    assert applicant.first_name == 'Jonathan'


def test_get_applicant(fixture_get_ws):
    ws = fixture_get_ws('drop_dups', autosetup=False)
    ws.drop_dups()
    applicants = applicant_classes.Applicants(ws)
    value = 43243
    applicant_found = applicants.get_applicant('wwid', value)
    assert applicant_found.last_name == "stay"
    value = value * 100
    applicant_not_found = applicants.get_applicant('wwid', value)
    assert applicant_not_found is None
