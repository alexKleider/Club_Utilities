#!/usr/bin/env python3

# File: csvtools.py

import csv
import codecs

contacts_file = '../Lists/google.csv'
output_file = 'output.tmp'
nonmembers_file = 'nonmembers.tmp'
"""
 0:Full Name,         1:1st Name,             2:Middle Name,          3:Last Name,         4:Yomi Name,
 5:Given Name Yomi,   6:Additional Name Yomi, 7:Family Name Yomi,     8:Name Prefix,       9:Name Suffix,
10:Initials,         11:Nickname,            12:Short Name,          13:Maiden Name,      14:Birthday,
15:Gender,           16:Location,            17:Billing Information, 18:Directory Server, 19:Mileage,
20:Occupation,       21:Hobby,               22:Sensitivity,         23:Priority,         24:Subject,
25:Notes,            26:Group Membership,    27:E-mail 1 - Type,     28:E-mail 1 - Value, 29:E-mail 2 - Type,
30:E-mail 2 - Value, 31:Phone 1 - Type,      32:Phone 1 - Value
"""

i_full_name = 0
i_first_name = 1
i_middle_name = 2
i_last_name = 3
i_initials = 10
i_grp_membership = 26
i_email1 = 28
i_email2 = 30
i_phone = 32

contacts_reader = csv.reader(
    codecs.open(contacts_file, 'rU', 'utf-16'),
    dialect='excel')

main_list = []
nonames = []
second_email = []
with_initials = []
with_phone = []
nogroup = []
nonmembers = []

for row in contacts_reader:
    if row[i_email2]:
        second_email.append("{:<25} {}"
            .format(row[i_email1], row[i_email2]))
    if row[i_initials]:
        with_initials.append(row[i_initials])
    if row[i_phone]:
        with_phone.append("{}: {}"
            .format(row[i_full_name], row[i_phone]))
    if not row[i_full_name]:
        nonames.append(row[i_email1])
    else:
        if row[i_middle_name]:
            first_name = ("{} {}"
                .format(row[i_first_name], row[i_middle_name]))
        else:
            first_name = row[i_first_name]
        name = "{} {}".format(first_name, row[i_last_name])
        line = ("{:<20} {:<15} {:<13} {:<32}" .format(
            row[i_full_name], first_name, row[i_last_name], row[i_email1]))
        grp_entry = row[i_grp_membership]
        if grp_entry:
            grps = grp_entry.split(":::")
            groups = []
            for grp in grps:
                if grp.find("Contacts") > -1:
                    groups.append("Contact")
                if grp.find("LIST") > -1:
                    groups.append("LIST")
                if grp.find("Moorings") > -1:
                    groups.append("Mooring")
                if grp.find("DockUsers") > -1:
                    groups.append("DockUser")
                if grp.find("Kayak") > -1:
                    groups.append("Kayak")
            groups.sort()
#           if (("Contacts" in groups) and (not ("LIST" in groups))):
            if (not ("LIST" in groups)):
                nonmembers.append(name)
            group_memberships = ", ".join(groups)
            line = line + " " + group_memberships
        else:
            nogroup.append(name)
#       for i in range(4, len(row)):
#           if row[i]:
#               line = line + " " + str(i) + ':' + row[i]
        main_list.append(line)
if main_list:
    club_contacts = "Google contacts for Rod & Boat Club\n"
    print("\nSending {} to {}."
        .format(club_contacts, output_file))
    output = "\n".join(main_list)
    with open(output_file, 'w') as fileobj:
        fileobj.write(club_contacts)
        fileobj.write(output)
if len(nonames) > 1:
    print("\nNo Name emails:")
    for noname in nonames:
        print(noname)
if len(second_email) > 1:
    print("\nEntries with a second email:")
    for entry in second_email:
        print(entry)

if len(with_initials) > 1:
    print("\nEntries with initials:")
    for entry in with_initials:
        print(entry)

if len(with_phone) > 1:
    print("\nEntries with phone:")
    for entry in with_phone:
        print(entry)

if len(nogroup) > 1:
    print("\nEntries with no group:")
    for entry in nogroup:
        print(entry)

if len(nonmembers) > 1:
    not_members = "Contacts that are not members:"
    print("\nSending {} to {}."
        .format(not_members, nonmembers_file))
    nonmembers[0] = not_members 
    output = "\n".join(nonmembers)
    with open(nonmembers_file, 'w') as fileobj:
        fileobj.write(output)

