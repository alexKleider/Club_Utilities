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

import os
import sys
import shutil
import tarfile
import rbc as club

# First part just checks that there is a valid parameter
# and assigns it to <target> (the full path of the gzip file) and
# from that derives <src_dir> (just the name of the gzip file)
# and <holder_dir> (a temporary directory into which the non-repo
# files/directories will be unziped :
if len(sys.argv) !=2:
    print("Must provide a tar.gz file as a paramter!")
    sys.exit()
target = sys.argv[1]
src_dir = target.split('/')[-1]
print("Source directory is {}".format(src_dir))
parts = src_dir.split('.')
if len(parts) >= 3 and parts[-2:] == ['tar', 'gz']:
    holder_dir = parts[-3]
    print('Suffix is "{}" and temporary directory is "{}".'
          .format('.'.join(parts[-2:]), holder_dir))
else:
    print("Suffix isn't right!")
    sys.exit()
response = input("Continue? ")
if not (response and response[0] in ('y', 'Y')):
    sys.exit()

# Extract the tar file:
tar = tarfile.open(target)
tar.extractall()
tar.close()

# Check that we got what is expected:
expected_dirs = set(club.Club.NONREPO_DIRS)
existing_dirs = set(os.listdir(path='./{}'.format(holder_dir)))
if not expected_dirs == existing_dirs:
    print("Expected and existing list of directories don't match!")
    shutil.rmtree(holder_dir)
    sys.exit()


for folder in club.Club.NONREPO_DIRS:
    shutil.rmtree(folder)
    shutil.copytree(
        os.path.join(".", holder_dir, folder),
        os.path.join(".", folder),
#       dirs_exist_ok=True,
        )

# Clean up:
shutil.rmtree(holder_dir)
