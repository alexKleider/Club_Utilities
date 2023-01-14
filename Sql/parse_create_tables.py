#!/usr/bin/env python3

# File: parse_create_tables.py

inputfile = 'create_tables.sql'

def get_commands(in_file):
    with open(in_file, 'r') as in_stream:
        command = ''
        for line in in_stream:
            line = line.strip()
            if line.startswith('--'):
                continue
            command = command + line.strip()
            if line.endswith(';'):
                yield command[:-1]
                command = ''

print("Running parse_create_commands")
for command in get_commands(inputfile):
    print(command)
