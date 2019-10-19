from mentormatch.applicants.applicant import Applicant


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

    applicant = Applicant(ws, 0)
    print()
    print(applicant.first_name)
    print(applicant)
    assert applicant.first_name == 'Jonathan'
