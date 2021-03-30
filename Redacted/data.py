### code removed from data.py

redacted = '''
def gather_contacts4mutt(g_contacts_file='~/Downloads/contacts.csv',
                         muttalias='~/.muttalias'):
    """
    <g_contacts_file> is a google contacts.csv file.
    Selects needed information and creates a muttalias file.
    This file can then be specified in ~/.muttrc as follows:
    set alias_file="~/.muttalias"
    """
    ret = []
    line = "alias {alias} {muttname} <{g_email}>"
    in_file = os.path.expanduser(g_contacts_file)
    out_file = os.path.expanduser(muttalias)
    with open(in_file, 'r', encoding='utf-8') as file_obj:
        reader = csv.DictReader(file_obj)
        for rec in reader:
            new_rec = get_gmail_record(rec)
            entry = line.format(**new_rec)
            if entry.count('<') > 1:
                print("data.gather_contacts4mutt error: {}".format(
                                                            entry))
            if new_rec['g_email']:
                ret.append(entry)
    with open(out_file, 'w') as file_obj:
        file_obj.write('\n'.join(ret))
'''

redacted = '''
def ck_applicants_cmd():
    """
    Driver for ck_applicants function.
    """
    club = Club()
    gather_contacts_data(club)
    gather_membership_data(club)
    a_by_status = gather_applicant_data(
            club.APPLICANT_SPoT)['applicants']
    ret = []
    g_set = club.g_by_group[club.APPLICANT_GROUP]
    m_set = set()  # applicants per the membership db
    a_set = set()  # applicants per the applicant SPoT

    if club.ms_by_status == a_by_status:
        ret.append("\n Club records match applicant SPoT")

    for key in club.ms_by_status:
        if 'a' in key:
            m_set = m_set.union(club.ms_by_status[key])
    for key in a_by_status:
        if 'a' in key:
            a_set = a_set.union(a_by_status[key])
    if g_set == m_set:
        ret.append("\nContacts match Club records.")
    else:
        ret.append("\nContacts do NOT match Club records.")
    if g_set == a_set:
        ret.append("\nContacts match applicant file.")
    else:
        ret.append("\nContacts do NOT match applicant file.")

    ck_applicants(club, a_by_status)
'''
