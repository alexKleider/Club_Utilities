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
    ./archive.py [(-o | -O) -q (-m | -a)]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -a --all  Back up all data! (Includes stable data)
  -q --quiet  Supress printing of files found to archive.
  -m --mail_only  Only archive mail, not rest of data.
  -O --Options  Show options and exit. Used for debugging.
  -o --options  Show options then continue.  ..ditto..

Unless -m or -a are set, data +/- mail (if it exists) are backed up.
If -m is set, only mail is backed up.
If -a is set, all (data, stable data and mail) are backed up.
"""

import os
import sys
import shutil
import tarfile
import datetime
from docopt import docopt
import rbc
import helpers

VERSION = '0.0.1'

args = docopt(__doc__, version=VERSION)

date_template = "%y-%m-%d_%H-%M"
today = datetime.datetime.today()
date_stamp = today.strftime(date_template)
#email_file = rbc.Club.JSON_FILE_NAME4EMAILS  # ../Data/emails.json
#letters_dir = rbc.Club.MAILING_DIR  # ../Data/MailingDir
mailing_sources = rbc.Club.MAILING_SOURCES
data_sources = (rbc.Club.DATA_DIR, )  # list of 1 dir: ../Data
stable_sources = rbc.Club.STABLE_DATA
data_destination = rbc.Club.DATA_ARCHIVE
mailing_destination = rbc.Club.MAILING_ARCHIVE
stable_destination = rbc.Club.STABLE_ARCHIVE
info_file = rbc.Club.ARCHIVING_INFO


def archive(sources,
            destination_directory,
            targz_base_name=date_stamp,
            quiet=False):
    """
    All files and directories listed in <sources> are archived into
    <targz_base_name>.tar.gz which is placed into
    <destination_directory>.
    Returns False if there are any irregularities, else returns True.
    A 'False' return does not necessarily mean that archiving failed.
    Returns 'True' if archiving is done.
    A temporary <targz_base_name> directory is created and may get
    left behind if irregularities occur or user aborts.
    If <quiet> is set to <True> no user interaction is done.
    """
    ret = True  # return value => "False" if irregularities occur
    copied = False  # nothing copied (yet)
    tar_file = "{}.tar.gz".format(targz_base_name)
    new_path = os.path.join(destination_directory,
                            tar_file)  # full path name of archive
    if os.path.exists(new_path):  # Unlikely if using defaults
        print("Specified tar file already exists...")
        print("... '{}'.".format(new_path))
        return False  # won't overwrite an existing tar file.
    try:   # base_name defaults to a time stamp
        os.mkdir(targz_base_name)  # create a temporary dir
    except FileExistsError:  # Unlikely if using defaults
        print("Temporary directory '{}' already exists."
              .format(targz_base_name))
        return False
    for source in sources:
#       print("source: '{}'".format(source))
#       print("targz_base_name: '{}'".format(targz_base_name))
        dest = os.path.join(targz_base_name,  #} file name
                os.path.split(source)[1])     #} by itself.
#       print("dest: '{}'".format(dest))
        if not quiet:
            response = input(
                "Move '{}' into '{}'? (y/n) ".format(source, dest))
            if not (response and response[0] in {'y', 'Y'}):
                ret = False
                print("... failed to move '{}' into '{}'!"
                        .format(source, dest))
                continue
        if os.path.isfile(source):
            shutil.copy2(source, dest)
            copied = True
            if not quiet:
                print("... copied file '{}' into '{}'"
                        .format(source, dest))
        elif os.path.isdir(source):
            shutil.copytree(source, dest)
            copied = True
            if not quiet:
                print("... copied directory '{}' into '{}'"
                        .format(source, dest))
        else:
            if not quiet:
                ret = False
                print("... no file or directory named '{}' exists."
                  .format(source))
    if copied:  # something has been copied over so archive
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(targz_base_name)
#       print("{} exists? {}".format(tar_file, os.path.isfile(tar_file)))
        if not quiet:
            print("Moving {} into {}..."
                .format(tar_file, destination_directory))
        move_res = shutil.move(tar_file, destination_directory)
#       if not quiet:
#           print("shutil.move({}, {}) returned {}"
#                   .format(tar_file, destination_directory, move_res))
    if not quiet:
        print("Removing temporary dirctory tree {}.".format(targz_base_name))
    shutil.rmtree(targz_base_name)
    return ret


def archive_mail(sources,
                 destination_directory,
                 targz_base_name=date_stamp):
    # let's not bother archiving an empty mailing directory:
    targets = [source for source in sources if (
        os.path.isfile(source) or (
        os.path.isdir(source) and os.listdir(source)))]
    if not args['--quiet']:
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
                        print("NOTE!",
                            "Failed to find '{}' to delete!"
                            .format(source))
            mail_action = 'mail'
        else:
            print("Mailing targets found but archive returned False!")
            return False
    else:
        print("No mailing <targets found to archive.")
        return False
    return '** archive_mail() => "success"'


def main():
    report = []
    action_keys = ('mail', 'volatile data', 'stable data', )
    actions = {k: True for k in action_keys}
    if args['--mail_only']:
        actions['volatile data'] = False
        actions['stable data'] = False
    elif not args['--all']:
        actions['stable data'] = False

    # check that an info file (record of past backups) exists
    # read and report if it does
    # if not provide for creation later (once know what to report.)
    try:
        with open(info_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        mode = 'w'  # will be creating a new file
        response = input(
            "file '{}' doesn't exist; continue? "
            .format(info_file))
    else:
        mode = 'a'  # will be appending
        lines = helpers.loose_trailing_empty_strings(
                                content.split('\n'))
        last_line = lines[-1] 
        response = input(
                'Date and details of last update: {}; continue?(y/n) '
                         .format(last_line))
    if not (response and response[0] in 'yY'):
        sys.exit()

    res = archive_mail(mailing_sources,
            mailing_destination)
    if res:
        report.append("mail")
    else:
        report.append("mail?")
    if not args['--quiet']:
        print("archive_mail() returns {}".format(res))

    if actions['volatile data']:
        res = archive(data_sources, data_destination)
        if res:
            report.append("data")
        else:
            report.append("data?")
        if not args['--quiet']:
            print("archiving data returns {}".format(res))

    if actions['stable data']:
        res = archive(stable_sources, stable_destination)
        if res:
            report.append("stable data")
        else:
            report.append("stable data?")
        if not args['--quiet']:
            print("archiving stable data returns {}".format(res))

    description = ' & '.join([text for text in report])
    with open(info_file, mode) as f:
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
