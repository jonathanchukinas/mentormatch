""""""

# --- Standard Library Imports ------------------------------------------------
# None

# --- Third Party Imports -----------------------------------------------------
import pandas as pd

# --- Intra-Package Imports ---------------------------------------------------
from mentormatch import matching


def test_mentees_tentative_mentors(fixture_applicants):
    preferred_matching = matching.PreferredMatching(fixture_applicants, autosetup=False)
    # preferred_matching.add_to_mentees_tentative_mentors()
    mentees = fixture_applicants['mentees']
    df = mentees.ws.df
    df['dummy'] = [None, 1, 2, 3]

    # --- jonathan wwids --------------------------------------------------------
    mentors = fixture_applicants['db']
    mentors_df = mentors.ws.df
    mentor_wwids = mentors_df['wwid']
    print()
    print(mentor_wwids)


    col = 'preferred_wwids'
    print()
    print(df)
    print(df['preferred_wwids'])
    df_pref_wwids = df['preferred_wwids'].notnull()
    print(df_pref_wwids)
    print(df[df_pref_wwids]['preferred_wwids'])
    print()
    # print(mentees.ws.df['tentative_mentor_ids'])
    johnny = mentees[0]
    johnnys_pref_wwids = johnny.preferred_wwids
    print(johnnys_pref_wwids)
    assert johnnys_pref_wwids is pd.np.nan

    timmy = mentees[2]
    timmys_pref_wwids = timmy.preferred_wwids
    print(type(timmys_pref_wwids))

