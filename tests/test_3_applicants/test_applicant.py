""""""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
# None

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import applicant as applicant_classes


def test_applicant_init(fixture_get_ws):
    applicant_classes.SingleApplicant(
        worksheet=fixture_get_ws('drop_dups', autosetup=False),
        index=0)


def test_applicant_getattr(fixture_get_ws):
    applicant = applicant_classes.SingleApplicant(
        worksheet=fixture_get_ws('drop_dups', autosetup=False),
        index=0)
    assert applicant.first_name == 'Jonathan'


def test_get_applicant(fixture_get_ws):
    ws = fixture_get_ws('drop_dups', autosetup=False)
    ws.drop_dups()
    applicants = applicant_classes.GroupApplicants(ws)
    value = 43243
    applicant_found = applicants.get_applicant('wwid', value)
    assert applicant_found.last_name == "stay"
    value = value * 100
    applicant_not_found = applicants.get_applicant('wwid', value)
    assert applicant_not_found is None
