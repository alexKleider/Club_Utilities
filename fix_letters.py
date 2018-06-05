#!/usr/bin/env python3

# File: fix_letters.py

import os
import sys

target_dir = sys.argv[1]
print(target_dir)

for letter_name in os.listdir(target_dir):
    path_name = os.path.join(target_dir, letter_name)
    lines = []
    with open(path_name, 'r') as file_obj:
        line_number = 0
        for line in file_obj:
            line_number += 1
            if line_number == 7:
                lines.extend(["\n", "\n"])
            if line_number == 12:
                lines.append("\n")
            if line:
                lines.append("     " + line.strip())
            else:
                lines.append(line)
    with open(path_name, 'w') as file_obj:
        file_obj.write("\n".join(lines))


