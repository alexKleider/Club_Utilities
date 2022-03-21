#!/usr/bin/env python3

# File: archive.py

"""
Initially began as a rewrite of archive-data.sh primarily to utilize
constants defined in rbc.py (such as 'rbc.Club.NONREPO_DIRS' rather
than hard code them into the utility- adhere to SPoT.)
Note: Assumes only defaults have been used in data management!

Also serves to replaces archive_mailing.sh.

It's inverse is restore.py. (still a work in progress)

Usage:
    ./archive.py [-h | --version]
    ./archive.py [(-o | -O) -q (-m | -d)]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -a --all  Back up all data! (Includes stable data)
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

VERSION = '0.0.1'

args = docopt(__doc__, version=VERSION)

date_template = "%y-%m-%d_%H-%M"
today = datetime.datetime.today()
date_stamp = today.strftime(date_template)
email_file = rbc.Club.JSON_FILE_NAME4EMAILS  # ../Data/emails.json
letters_dir = rbc.Club.MAILING_DIR  # ../Data/MailingDir
mailing_sources = [email_file, letters_dir]
list_of_data_targets = [rbc.Club.DATA_DIR]  # list of 1 dir: ../Data
data_destination = os.path.expandvars(
    '$CLUB/Archives/Data')
mailing_destination = os.path.expandvars(
    '$CLUB/Archives/Mailing')
info_file = os.path.expandvars(
    "$CLUB/Info/last")


def archive(sources,
            destination_directory,
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
    try:              # base_name defaults to a time stamp
        os.mkdir(targz_base_name)  # create a temporary dir
    except FileExistsError:
        print("Temporary directory '{}' already exists."
              .format(targz_base_name))
        return False
    for source in sources:
#       print("source: '{}'".format(source))
#       print("targz_base_name: '{}'".format(targz_base_name))
        dest = os.path.join(targz_base_name,
                os.path.split(source)[1])
#       print("dest: '{}'".format(dest))
        if not args["--quiet"]:
            print("source & dest are {} & {}".format(source, dest))
            response = input("Continue? (y/n) ")
            if not (response and response[0] in {'y', 'Y'}):
                sys.exit()
        if os.path.isfile(source):
            shutil.copy2(source, dest)
            ret = True
            if not args['--quiet']:
                print("   Copied file '{}' into '{}'"
                        .format(source, dest))
        elif os.path.isdir(source):
            shutil.copytree(source, dest)
            ret = True
            if not args['--quiet']:
                print("   Copied directory '{}' into '{}'"
                        .format(source, dest))
        else:
            if not args['--quiet']:
                print("   No file or directory named '{}' exists."
                  .format(source))
    if ret:  # something has been copied over so archive
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(targz_base_name)
#       print("{} exists? {}".format(tar_file, os.path.isfile(tar_file)))
        if not args['--quiet']:
            print("Moving {} info {}..."
                .format(tar_file, destination_directory))
        move_res = shutil.move(tar_file, destination_directory)
        if not args['--quiet']:
            print("shutil.move({}, {}) returned {}"
                    .format(tar_file, destination_directory, move_res))
    if not args['--quiet']:
        print("Removing dirctory tree {}.".format(targz_base_name))
    shutil.rmtree(targz_base_name)
    return ret


def archive_mail(sources,
                 destination_directory,
                 targz_base_name=date_stamp):
    # let's not bother archiving an empty mailing directory:
    targets = [source for source in sources if (
        os.path.isfile(source) or (
        os.path.isdir(source) and os.listdir(source)))]
    print("<targets> set to '{}'".format(targets))
    if targets:
        if archive(targets, destination_directory):
            ans = input(
                  "Mailing archived.  Delete mailings from data? ")
            if ans and ans[0] in {'y', 'Y'}:
                for source in sources:
                    print("within archive_mail: deleting {}"
                            .format(source))
                    if os.path.isdir(source):
                        shutil.rmtree(source)
                    elif os.path.isfile(source):
                        os.remove(source)
                    else:
                        print("ABORTING!",
                            "Something not right in archive_mail!")
                        sys.exit()
            args['mail_action'] = 'mail'
        else:
            print("Mailing targets found but archive returned False!")
            return False
    else:
        print("No mailing <targets found to archive.")
        return False


def loose_trailing_empty_strings(list_of_strings):
    if list_of_strings:
        while not list_of_strings[-1]:
            list_of_strings = list_of_strings[:-1]
    return list_of_strings

def main():
    args['mail_action'] = ''
    args['data_action'] = ''
    # decide if we are appending ('a') or creating a new ('w') file:
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
        response = input('last update was {}; continue? y/n '
                         .format(last_line))
    if not (response and response[0] in 'yY'):
        sys.exit()

    res = archive_mail(mailing_sources,
                       mailing_destination)
    if not args['--quiet']:
        print("archive_mail() returns {}".format(res))
    if args['--mail_only']:
        return

    if archive(list_of_data_targets, data_destination):
        args['data_action'] = 'data'
    description = ' & '.join([text for text in (
        args['mail_action'], args['data_action']) if text])
    with open(info_file, action) as f:
        f.write("\n{} {}".format(date_stamp,
                               " {} archived".format(description)))


if __name__ == '__main__':
    if args['--options'] or args['--Options']:
        print("Arguments are as follows:")
        for arg in args:
            print("\t{}: {}".format(arg, args[arg]))
        if args['--Options']:
            sys.exit()
    main()
