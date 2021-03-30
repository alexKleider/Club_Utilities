import data
import rbc
import member

club = rbc.Club()
club.no_email = []
data.gather_membership_data(club)
data.gather_contacts_data(club)
#for item in club.__dict__: print(item)
#_ = input("any key to continue ")

def compare_dicts(d1, d2,
                  d1_name='name1', d2_name='name2',
                  special_key=None,
                  special_key_listing=None):
    """
    Compares two dictionaries and returns any instances in which a key
    in one yields a value different from the same key in the other, or
    a key in the first is not present in the second.
    Optionally it can also provide for a listing of a specified key.
    """
    ret = []
    for key1 in d1:
        val1 = d1[key1]
        if (val1==special_key and special_key
            and isinstance(special_key_listing, list)):
            special_key_listing.append(key1)
        else:
            try:
                val2 = d2[key1]
            except KeyError:
                ret.append("no {} entry for {} ({})"
                           .format(d2_name, key1, val1))
            else:
                if val1 != val2:
                    ret.append(
                        "key ({}) value mismatch ({}, {})"
                        .format(key1, val1, val2))
    return ret


m_gmail_mismatch = compare_dicts(club.ex_db_emails,
                                 club.gmail_by_name,
                                 "member data base", "gmail",
                                 special_key=member.NO_EMAIL_KEY,
                                 special_key_listing=club.no_email)
if m_gmail_mismatch:
    print("\nThere are the following member DB/gmail disparities:")
    print('\n'.join(m_gmail_mismatch))
else:
    print("\nNo member DB/gmail missmatches.")

gmail_m_mismatch = compare_dicts(club.gmail_by_name,
                                 club.ex_db_emails,
                                 "gmail", "member data base")
if gmail_m_mismatch:
    print("\nThere are the following gmail/member DB disparities:")
    print('\n'.join(gmail_m_mismatch))
else:
    print("No gmail/member DB missmatches.")

if club.no_email:
    print("\nNo email available for the following {} Club members:"
          .format(len(club.no_email)))
    print('\n'.join(club.no_email))
