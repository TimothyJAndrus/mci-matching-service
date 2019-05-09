from itertools import combinations

from matching.database import engine, individual, session

def compute_match_with_score(individual_args: dict):
    """
    This function determines (1) if incoming data for an Individual
    can be reasonably matched with an existing entry, and (2) the
    score assigned to the likelihood of matching. 

    Implicit in this logic: the `first_name` and `last_name` are weighted at 0.2 (or 0.4 together)
    and each remaining field are weighted at 0.1. Note! The precise weights for these fields
    will be fine tuned, as we come to understand the data better.

    :param individual_args: a dict of Individual data that includes, at minimum, a
    `first_name` and `date_of_birth`.

    :returns: an Individual and a score of the match likelihood (or None) 
    """

    mci_id = None
    score = None
    
    ssn = individual_args.get('ssn')
    if ssn: 
        ssn_last_four_digits = ssn[-4:]


    filters = {
        'last_name': individual_args.get('last_name'),
        'telephone': individual_args.get('telephone'),
        'gender_id': individual_args.get('gender_id'),
        'email_address': individual_args.get('email_address'),
        'mailing_address_id': individual_args.get('mailing_address_id'),
        'ssn': individual_args.get('ssn'),
        # 'ssn': like("%s{}".format(ssn_last_four_digits)) if ssn_last_four_digits else ssn,
        # TODO: how to query for last four digits of SSN, and move the logic further upstream
    }

    potential_matches = session.query(individual).filter_by(
        first_name=individual_args['first_name'],
        date_of_birth=individual_args['date_of_birth']
    )

    if potential_matches.first():
        score = 0.4
        list_of_combos = []
        # Find all filter combinations.
        # Reference: https://stackoverflow.com/questions/11905573/getting-all-combinations-of-key-value-pairs-in-python-dict
        for i in range(len(filters), 0, -1):
            list_of_combos += list(map(dict, combinations(filters.items(), i)))

        for combo in list_of_combos:
            match = potential_matches.filter_by(**combo)

            if match.first():
                # TO TEST can a `match` have more than one Individual?
                mci_id = match.first().mci_id
                score += len(combo) * 0.1
                break

    return mci_id, score