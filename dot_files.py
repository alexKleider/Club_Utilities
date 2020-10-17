#!/usr/bin/env python3

# File: dot_files.py

"""
There are 'dot files' that must be in ~/ to provide security
credentials for sending emails. These are not kept in the repo
or even on the backups (stored on the Club's Google Drive)
so must be reconstituted each time a system is set up.
This utility provides menu driven functionality to:
1. copy these files from a working system into a directory that 
can then be scp'ed to a new system providing it with the needed
files.
2. save an original copy of the .msmtprc file on the new system
preventing its loss when overwritten.
"""

import os
import sys
import shutil

menu = """
Chose one of the following:
    1: Collect needed security sensitive dot files > ~/Collector/.
    2: Save original version of ~/.msmtprc as ~/.msmtprc.original.
Choice: """

file_listing = """
-rw------- 1 alex alex  1145 May 27 11:54 .msmtprc
-rw------- 1 alex alex   775 May 28 11:34 .muttakg
-rw------- 1 alex alex   816 May 28 11:35 .muttclubg
-rw------- 1 alex alex   756 May 28 11:18 .mutteasy
-rw------- 1 alex alex   779 May 28 11:36 .muttsonic
-rw------- 1 alex alex    10 May 27 11:51 .pw.akg
-rw------- 1 alex alex     9 May 27 11:52 .pw.clubg
-rw------- 1 alex alex     9 May 27 11:51 .pw.easy
-rw------- 1 alex alex     9 May 27 11:51 .pw.sonic
"""

def _next_dot_file(file_listing=file_listing):
    for line in file_listing.split('\n'):
        if line:
            yield line.split()[-1]


def _create_dir(dir_name):
    try:
        os.mkdir(dir_name, mode=0o700)
    except FileExistsError:
        print("Directory '{}' already exists!".format(dir_name))
        sys.exit()


def _collect_dot_files(collecting_dir):
    for dot_file in _next_dot_file():
        source = os.path.expanduser('~/{}'.format(dot_file))
        print('\t'+source)
        shutil.copy(source, collecting_dir)


def _save_original_version(file_name, suffix):
    os.rename(file_name, file_name+suffix)


def rename_msmtprc(suffix):
    _save_original_version(os.path.expanduser('~/.msmtprc'), suffix)
    

def collect():
    collecting_dir = os.path.expanduser('~/{}'.format('Collector'))
    _create_dir(collecting_dir)
    _collect_dot_files(collecting_dir)
    return collecting_dir


def driver():
    response = input(menu)
    if response == '1':
        print('Required dot files:')
        print('have been copied into {}.'.format(collect()))
    elif response == '2':
        rename_msmtprc('original')
        print('"~/.msmtprc" has been renamed "~/.msmtprc.original"')
    else:
        print("Only valid choices are '1' or '2'.")


if __name__ == "__main__":
    driver()
