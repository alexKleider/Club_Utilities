#!/usr/bin/env python3

# File: gmail_fees.py

import json
import data
from rbc import Club

outfile = "gmail_fee_info.json"
club = Club()
club.quiet = True
data.gather_contacts_data(club)

collector = []
fee_groups = ["DockUsers", "Kayak", "Moorings"]
fee_set = set(fee_groups)
keys = sorted(club.groups_by_name.keys())
for key in keys:
    intersect = club.groups_by_name[key].intersection(fee_set)
    if intersect:
        renamed_group = []
        for category in intersect:
            if category == 'DockUsers':
                renamed_group.append('dock')
            if category == 'Kayak':
                renamed_group.append('kayak')
            if category == 'Moorings':
                renamed_group.append('mooring')
        if renamed_group:
            collector.append("{}: {}".
                    format(key, repr(set(renamed_group))))
with open(outfile, 'w') as stream:
    json.dump(collector, stream)
exit()
for item in collector:
    print(item)
