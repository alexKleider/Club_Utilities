#!/usr/bin/env python3

# File: archive.py

"""
A rewrite of archive-data.sh primarily to utilize
constants defined in rbc.py (such as 'rbc.Club.NONREPO_DIRS'
rather than hard code them into the utility- adhere to SPoT.)

Also replaces archive_mailing.sh.

It's inverse is restore.py.

Usage:
    ./archive.py [-h | --version]
    ./archive.py [(-o | -O) -q -m]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -q --quiet  Supress printing of files found to archive.
  -m --mail_only  Only archive mail, not rest of data.
  -O --Options  Show options and exit. Used for debugging.
  -o --options  Show options then continue.  ..ditto..
"""

import os
import sys
import shutil
import tarfile
import datetime
from docopt import docopt
import rbc

VERSION = '0.0.0'

date_template = "%y-%m-%d"
today = datetime.datetime.today()
date_stamp = today.strftime(date_template)
email_file = rbc.Club.JSON_FILE_NAME4EMAILS
letters_dir = rbc.Club.MAILING_DIR
mailing_sources = [email_file, letters_dir]
list_of_data_targets = rbc.Club.NONREPO_DIRS
data_destination = os.path.expandvars(
    '$CLUB/Archives/Data')
mailing_destination = os.path.expandvars(
    '$CLUB/Archives/Mailings')
info_file = os.path.expandvars(
    "$CLUB/NR/Info/last")


def archive(destination_directory,
            sources,
            targz_base_name=date_stamp,
            ):
    """
    Create a <targz_base_name>.tar.gz archive and
    file it in the <destination_directory>.
    The archive is to contain all files &/or directories listed
    in <sources> all under a directory called <targz_base_name>
    which is temporarily created (as a place to gather what is to
    be archived) and then deleted. Fails if such a directory already
    exists.
    Returns False if no archiving is done, else returns True.
    """
    ret = False
    tar_file = "{}.tar.gz".format(targz_base_name)
    new_path = os.path.join(destination_directory,
                            tar_file)
    if os.path.exists(new_path):
        print("Specified tar file already exists...")
        print("... '{}'.".format(new_path))
        return False
    try:
        os.mkdir(targz_base_name)  # create a temporary dir
    except FileExistsError:
        print("Temporary directory '{}' already exists."
              .format(targz_base_name))
        return False
    for source in sources:
        dest = os.path.join(targz_base_name, source)
        if not args["--quiet"]:
            print("source & dest are {} & {}".format(source, dest))
        if os.path.isfile(source):
            shutil.copy2(source, targz_base_name)
            ret = True
            if not args['--quiet']:
                print("   Archiving file '{}'".format(source))
        elif os.path.isdir(source):
            shutil.copytree(source, dest)
            ret = True
            if not args['--quiet']:
                print("   Archiving directory '{}'".format(source))
        else:
            if not args['--quiet']:
                print("   No file or directory named '{}' exists."
                  .format(source))
    if ret:
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(targz_base_name)
#       print("{} exists? {}".format(tar_file, os.path.isfile(tar_file)))
        res = shutil.move(tar_file, destination_directory)
        if not (res == new_path):
            print("Archiving error!")
            ret = False
    shutil.rmtree(targz_base_name)
    return ret


def archive_mail(sources=mailing_sources):
    no_empties = [source for source in sources if (
        os.path.isfile(source) or (
        os.path.isdir(source) and os.listdir(source)))]
    print("within archive_mail() archiving: {}"
          .format(no_empties))
    if no_empties:
        if archive(mailing_destination, no_empties):
            ans = input(
                  "Mailing archived.  Delete mailings from data? ")
            if ans and ans[0] in {'y', 'Y'}:
                for source in sources:
                    if os.path.isdir(source):
                        shutil.rmtree(source)
                    elif os.path.isfile(source):
                        os.remove(source)
                    else:
                        print("Something not right in archive_mail!")
            args['mail_action'] = 'mail'
        else:
            print("No mailing found to archive.")
    else:
        print("No mailing found to archive.")


def loose_trailing_empty_strings(list_of_strings):
    if list_of_strings:
        while not list_of_strings[-1]:
            list_of_strings = list_of_strings[:-1]
    return list_of_strings

args = docopt(__doc__, version=VERSION)

def main():
    args['mail_action'] = ''
    args['data_action'] = ''
    if args['--options'] or args['--Options']:
        print("Arguments are as follows:")
        for arg in args:
            print("\t{}: {}".format(arg, args[arg]))
        if args['--Options']:
            sys.exit()
    try:
        with open(info_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        action = 'w'  # write (creating a new) file
        response = input(
            "file '{}' doesn't exist; continue? "
            .format(info_file))
    else:
        action = 'a'  # append to existing file
        lines = loose_trailing_empty_strings(content.split('\n'))
        last_line = lines[-1] 
        last_time = last_line[0]
        response = input('last update was {}; continue? y/n '
                         .format(last_line))
    if not (response and response[0] in 'yY'):
        sys.exit()

    res = archive_mail()
    if not args['--quiet']:
        print("archive_mail() returns {}".format(res))
    if args['--mail_only']:
        return

    if archive(data_destination, sources=list_of_data_targets):
        args['data_action'] = 'data'
    description = ' & '.join([text for text in (
        args['mail_action'], args['data_action']) if text])
    with open(info_file, action) as f:
        f.write("\n{} {}".format(date_stamp,
                               " {} archived".format(description)))


if __name__ == '__main__':
    main()
