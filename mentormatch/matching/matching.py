def preferred_matching():
    # TODO pseudocode - high level
    #   "Randomly" order the mentees (in a repeatable manner)
    #       Hash a wwid+year string
    #       Create a deque container containing just those mentee who listed preferred mentors
    #   For each mentee, check their list of preferred mentors
    #       add a new column: tentative_mentors.
    #       Convert preferred wwids to id (this involves checking to make sure that wwid actually exists"
    #       For each preferred mentor (id):
    #           make sure the mentee doesn't violate any of the mentor's deal breakers
    #               (such as mentee's site not being on the mentor's yes or maybe site lists)
    #   For each mentor, create a column `tentative_mentees`
    #   Take first mentee off the deque:
    #       Assign them to their most preferred mentor.
    #       Sort all mentees assigned to this mentor by tie breaker (maybe use another deque?)
    #       If mentor is still under capacity, stop. Move to next mentee in deque
    #       Elif that takes the mentor above capacity, take the mentee who scores lowest on the tie breaker
    #           If that mentee is the same as the one we took of the deque:
    #               repeat the above with their next preferred mentor
    #           elif the removed mentee is a different one, add mentee to end of deque and:
    #               if mentee has a priority level, increment their priority
    #               else: modify this mentee's tentative_mentors list, removing this and higher-ranked mentors.
    #                   (There's no way they can now win these mentors)
    #       If mentee get to end of their tentative mentors (they' couldn't be successfully matched):
    #           If mentee has a priority level, increment, add to end of deque
    #           Else: Let this mentee fall out of the process. She'll get priority during random pairings.
    #       Repeat.
    #
    #
    #
    # TODO pseudocode for random pairing
    #   give priority to:
    #       1) Those marked with priority
    #       2) Those who chose preferred mentors but didn't receive one.
    #
    #
    #
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
            mentor = self.__roster.get_single_applicant(wwid)
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
