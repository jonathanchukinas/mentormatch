from mentormatch.applicants.applicant_base import ApplicantBase


def are_different_people(mentor: ApplicantBase, mentee: ApplicantBase):
    return mentor != mentee,


def mentor_sees_no_dealbreakers(mentor: ApplicantBase, mentee: ApplicantBase):
    return len(mentor.preference_no & mentee.location_and_gender) == 0


def mentee_sees_no_dealbreakers(mentor: ApplicantBase, mentee: ApplicantBase):
    return len(mentee.preference_no & mentor.location_and_gender) == 0


def match_count(self, chooser_type: str, pref_suffix):
    chooser_attr = 'preference_' + pref_suffix  # e.g. 'preference_yes'

    chooser_obj = getattr(self, chooser_type)
    chooser_pref = set(
        chooser_obj[chooser_attr])  # chooser's preferences e.g. (horsham, female, male, west_chester)

    target_type = other_type(chooser_type)
    target_obj = getattr(self, target_type)
    target_char = set(target_obj.preference_self)  # target's characteristics e.g. (horsham, female)

    overlapping_items = chooser_pref & target_char
    count_overlap = len(overlapping_items)  # count of target characteristics desired by chooser
    return count_overlap
