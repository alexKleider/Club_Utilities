

def ck_integrity():
    """
    Working on a function that will check the integrity of the Club's
    data base(s.)  It will combine the ck_fields and compare_gmail
    commands and also possibly check for consistency with the
    'extra_fees'/'extra_charges', 'stati', ... etc categories.
    """
    # Set up collectors by name and by email each
    # for gmail and for memlist db.
    # 'names' will be (last, first) tuples.
    g_by_name = dict()
    g_by_email = dict()
    m_by_name = dict()
    m_by_email = dict()

