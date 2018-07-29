# File: users.py

"""
Using the file "extra-fees.txt" as input, this little
utility prints out a table showing members who pay for
mooring, dock use, and/or kayak storage.
Typical usage:
    $ python usage.py > extra-fees.tbl
"""

infile = "extra-fees.lst"

dock_usage = []
mooring = []
kayak_storage = []
uninterpretable = []
n_longest = 0

with open(infile, "r") as f_obj:
    for line in f_obj:
        if 'mooring' in line:
            current = mooring
        elif 'dock' in line:
            current = dock_usage
        elif 'kayak' in line:
            current = kayak_storage
        else:
            split_line = line.split()
            if len(split_line) == 3:
                first = split_line[0]
                last = split_line[1][:-1]
                amt = int(split_line[2])
                new_line = "{}, {}: ${}".format(first, last, amt)
                current.append(new_line)
            else:
                uninterpretable.append(line)

if len(dock_usage) > n_longest:
    n_longest = len(dock_usage)
if len(mooring) > n_longest:
    n_longest = len(mooring)
if len(kayak_storage) > n_longest:
    n_longest = len(kayak_storage)
final = (
        ["Dock Usage", "----------"] + [""] * n_longest,
        ["Mooring", "-------"] + [""] * n_longest,
        ["Kayak Storage", "-------------"] + [""] * n_longest
        )
for i in range(n_longest):
    try:
        final[0][i+2] = dock_usage[i]
        final[1][i+2] = mooring[i]
        final[2][i+2] = kayak_storage[i]
    except IndexError:
        pass

print()
print("Members Paying Fees For Extra Privileges")
print("========================================")
for i in range(n_longest + 1):
    print("{:<25} {:<25} {:<25}"
        .format(final[0][i], final[1][i], final[2][i]))

