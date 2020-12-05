#!/usr/bin/env python3

# File: restore.py

"""
Usage:
  restore.py src 

Requires one parameter, the name of a tar.gz file
which is assumed to be one that has been generated
by the archive_data.sh script.
Replaces the non-repo files under the repo directory.
"""

import tarfile
import sys
if len(sys.argv) !=2:
    print("Must provide a tar.gz file as a paramter!")
    sys.exit()
target = sys.argv[1]
src_dir = target.split('/')[-1]
print("Source directory is {}".format(src_dir))
parts = target.split('.')
if len(parts) >= 2 and parts[-2:] == ['tar', 'gz']:
    print('Ok to procede (suffix is "' +
          '.'.join(parts[-2:]) + '")')
else:
    print("Suffix isn't right!")
    sys.exit()
response = input("Continue? ")
if response and response[0] in ('y', 'Y'):
    pass
else:
    sys.exit()
tar = tarfile.open(target)
tar.extractall()
tar.close()

