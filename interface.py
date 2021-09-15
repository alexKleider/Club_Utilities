#!/usr/bin/env python3

# File: interface.py   The curses interface.

"""
Notes:

Some day I'll create a curses interface to the utils utility.
Have begun in earnest (Sept 2021)
"""

import curses as cur
import utils as u

WIDTH = 30
HEIGHT = 10
KEY_RETURN = 10
ESC = 27
QUIT = 137  # Q)uit (ascii for lower case "q")

options = {
        'ck_data': ('-d', '-i', '-A', '-S', '-X', '-C', '-o', ),
            # -d -i <infile> -A <app_spot> -S <sponsors_spot> -X <fees_spot> -C <contacts_spot> -o <outfile>
            # -d   Include details: fee inconsistency for ck_data,
        'payables': ('-T', '-w', '-i', '-o', ),
            # -T -w <width> -i <infile> -o <outfile>
        'show': ('-i', '-A', '-S', '-o', ),
            # -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>
        'report': ('-i', '-A', '-S', '-o'),
            # -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>
        'stati': ('-O', '-D', '-M', '-B', '-s', '--mode', '-i', '-A', '-S', '-o', ),
            # -D -M -B -s stati --mode <mode> -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>
        }

# The following are globals:
highlight = 0
cmd_name = None
ncmd_name = None
invalid_choice = False  


def option_listing(cmd):
    """
    Provides a list of strings showing the options and
    their current values for the specified command.
    Ordered as they appear in their respective tuples.
    (See <options> above.)
    """
    ret = []
    for item in options[cmd]:
        ret.append("{}: {}".format(item, u.args[item]))
    return ret


def get_noptions(cmd):
    return len(options[cmd])


def print_menu(m_win, choices, hlight):
        x = y = 2
        m_win.box()
        m_win.addstr(1,x,
                     "Up & Down arrows to edit, <esc> when done: ",
                     cur.A_BOLD)
        for n, choice in enumerate(choices, 1):
            if hlight == n:  # Highlight the present choice
                m_win.addstr(y,x, "{}".format(choice),
                        cur.A_REVERSE)
            else:
                m_win.addstr(y,x, "{}".format(choice))
            y += 1
        m_win.clrtoeol()
        m_win.refresh()

def main(scr):
    global highlight
    global cmd_name
    global ncmd_name
    global invalid_choice
    scr.clear()
    maxy, maxx = scr.getmaxyx()

    # decide which command to execute:
    scr.addstr("Welcome to the Bolinas Rod & Boat Club Utilities")
    scr.clrtoeol()
    scr.addstr(1,0, "Available commands are as follows:", cur.A_BOLD)
    scr.clrtoeol()
    cmds = {
            'ck_data': u.ck_data_cmd,
            'payables': u.payables_cmd,
            'show': u.show_cmd,
            'report': u.report_cmd,
            'stati': u.stati_cmd,
            }
    cmd_names = sorted(cmds.keys())
    ncmd_names = len(cmd_names)
    # present user with a listing of commands available...
    for n, cmd_name in enumerate(cmd_names, 1):
        scr.addstr(n+1, 4, 
                   "{}: {}".format(n, cmd_name))
        scr.clrtoeol()
    scr.addstr(2+ncmd_names,0, 'Choose command #: ', cur.A_BOLD)
    scr.clrtoeol(); scr.refresh()
    while True:
        try:
            ncmd_name = int(chr(scr.getch()))-1  ## WHAT if non integer?  DEBUG
        except ValueError:
            scr.addstr(2+ncmd_names,0,
                       'Invalid choice- try again: ',
                       cur.A_BOLD)
            scr.clrtoeol()
            scr.refresh()
        else:
            if ((ncmd_name >= 0)            # }  valid
            and (ncmd_name < ncmd_names)):  # }  choice
                scr.addstr(2+ncmd_names,0, '    ')
                scr.clrtoeol()
                break
            else:
                scr.addstr(2+ncmd_names,0,
                           'Invalid choice- try again: ',
                           cur.A_BOLD)
                scr.clrtoeol()
                scr.refresh()

    # we've established which command to run (so set up for it...)
    cmd_name = cmd_names[ncmd_name]
    cmd_func = cmds[cmd_name]
    n_options = get_noptions(cmd_name)
    # Notify user of choice made:
    scr.addstr(3+ncmd_names, 0,
               "You've chosen to execute '{}' command ..."
               .format(cmd_name))
    scr.clrtoeol(); scr.refresh()
    # may want to change options so
    # initialize option changing application data:
    opt_win = cur.newwin(n_options+3, maxx,
                         4+ncmd_names,0)
    opt_win.keypad(True)
    highlight = 1
    choice = 1
    choice_fmt = "Edit option %d. %s\n"
    scr.addstr(4+ncmd_names, 0,
               "...but first select, edit & confirm options:")
    scr.clrtoeol()
    scr.addstr(cur.LINES-1,0,
               "Here's where we'll print character pressed")
    scr.clrtoeol()
    scr.refresh()

    # event loop:
    while True:
        scr.addstr(5+ncmd_names,1,
                "Up & Down arrows to edit, <esc> when done: ",
                cur.A_BOLD)
        scr.clrtoeol(); scr.refresh()
        print_menu(opt_win, option_listing(cmd_name),
                   highlight)
        c = opt_win.getch()
        cy, cx = opt_win.getyx()
        if c == cur.KEY_UP:
            if highlight == 1:
                highlight = n_options  # move hl to bottom
                opt_win.move(n_options,0)
            else: highlight -= 1
            opt_win.move(highlight,0)
        elif c == cur.KEY_DOWN:
            if highlight == n_options:
                highlight = 1  # move hl to top
                opt_win.move(highlight,0)
            else: highlight += 1
            opt_win.move(highlight,0)
        elif c in (KEY_RETURN, cur.KEY_ENTER):
#           elif c == KEY_RETURN:
            choice = highlight  # <choice> has been made
            scr.addstr(cur.LINES-2,0,
                    choice_fmt%(choice, 
                    option_listing(cmd_name)[choice-1]))
            scr.clrtoeol()
            # edit the chosen option here
            scr.getch()
        elif c == ESC:  # escape character
            scr.addstr(cur.LINES-1,0,
               "Finished editing options!! (any key to continue)")
            scr.clrtoeol()
            scr.refresh()
            scr.getch()
            break
        else:
            scr.addstr(cur.LINES-1,0,
                       "Character pressed:%3d"%c)
            scr.clrtoeol()
            scr.refresh()

    scr.addstr(3+ncmd_names, 0,
               "About to execute '{}' command ..."
               .format(cmd_name))
    scr.clrtoeol(); scr.getch()
    cmd_func()

cur.wrapper(main)

# outside of curses reporting:
if invalid_choice:
    print("Your choice ({}) is out of range.".format(ncmd_name))
else:
    print("Ran '{}' command".format(cmd_name))
