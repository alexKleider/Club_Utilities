#!/usr/bin/env python3

# File: archive_data.py

"""
A rewrite of archive-data.sh primarily to utilize
rbc.Club.NONREPO_DIRS rather than hard code the names
into the utility.
It functions as the inverse to restore.py.

'x:gz'
Create a tarfile with gzip compression. Raise an FileExistsError
exception if it already exists.
"""

import os
import sys
import shutil
import tarfile
import datetime
import rbc

list_of_target_directories = rbc.Club.NONREPO_DIRS
date_template = "%y-%m-%d"
today = datetime.datetime.today()
date_stamp = today.strftime(date_template)


def archive(destination_directory,
            source = list_of_target_directories,
            targz_base_name = date_stamp
            ):
    """
    Fails if a directory <date_stamp> already exists.
    """
    print(date_stamp)
    os.mkdir(targz_base_name)
    for folder in list_of_target_directories:
        shutil.copytree(folder,
                        os.path.join(targz_base_name, folder),
                        )
    tar_file = "{}.tar.gz".format(targz_base_name)
    with tarfile.open(tar_file, "w:gz") as tar:
        tar.add(targz_base_name)

    shutil.rmtree(targz_base_name)

    res = shutil.move(tar_file, destination_directory)
    if not (res == destination_directory):
        print("The following two strings:")
        print("\t'{}'".format(res))
        print("\t'{}'".format(os.path.join(destination_directory,
                            tar_file)))
        print("are not equal!! Beats me why!")

if __name__ == '__main__':
    archive(os.path.expandvars("$CLUB/Archives/Data"),
            )
    with open("Info/last", 'w') as f:
        f.write(date_stamp)
