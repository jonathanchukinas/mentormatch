def preferred_matching():
    # TODO pseudocode
    #   This serves mostly (only?) to compare one potentially pairing with another.
    #   Comparisons are based on:
    #   Ties are broken in the following order (starting with the first):
    #       1 - Mentor preferences (site, gender). A mentee who has more "yes"es break the tie.
    #       2 - Level difference: A smaller level difference wins.
    #       3 - Rank Order: Whichever mentee ranked this mentor higher wins.
    #       4 - Count of preferred wwids: The mentee who listed more preferred wwids wins.
    #       5 - History - the mentee who's been rejected the most or had the least number of mentors wins
    #       6 - Priority - mentees who were rejected last year fall into this category.
    #               These are the ones we want badly to match up this year.
    #               This one has the potential to move up the tiebreaker order.
    #               If, for example, we arrive at the end and there are 'priority' mentees
    #       7 - First applied - probably will only rarely come up, but there needs to be some final tie breaker...
    #   There are other factors I brainstormed, but they won't be used during the preferred matching phase.
    #       Random vs. Preferred Pairing -- not used in preferred matching
    #       Does the Mentee want a random pairing at all? -- not used in preferred matching
    #       Mentee preferences (site, gender)  -- not used in preferred matching

    # Randomize mentees with preferred wwids into a queue
    mentees = self.__mentees
    mentees = [mentee for mentee in mentees if mentee.has_preferred_mentors()]
    mentees.sort(key=lambda mentee: mentee.get_hash(current_year))
    mentee_queue = deque(mentees)
    del mentees

    while 0 < len(mentee_queue):
        mentee = mentee_queue.popleft()
        for wwid in mentee.preferred_wwids():
            mentor = self.__roster.get_applicant_by_wwid(wwid)
            rejected_mentee = mentor.add_mentee(mentee)
            if rejected_mentee is None:
                # Success!
                # Mentor still had capacity, therefore accepted this mentee
                break
            elif rejected_mentee != mentee:
                # Success!
                # Mentor didn't have capacity, but this mentee was better than at least one of the
                #   mentor's existing mentees. Put that rejected mentee at the end of the queue:
                mentee_queue.append(rejected_mentee)
                break
            elif rejected_mentee == mentee:
                # Fail!
                # Mentor didn't have capacity, and this mentee wasn't a good enough match to beat out the other(s)
                #   already paired with this mentor.
                pass
            else:
                logging.debug('Mentor rejected something other than None, next_mentee, or this mentee')
        mentee.could_not_find_a_match()
        if mentee.still_has_chances():
            mentee_queue.append(mentee)


def random_matching():
    pass
