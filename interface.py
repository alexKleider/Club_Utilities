#!/usr/bin/env python3

# File: interface.py   The curses interface.

"""
Notes:

Some day I'll create a curses interface to the utils utility.
Have begun in earnest (Sept 2021)
"""

import sys
import curses as cur
from curses.textpad import Textbox
import utils as u

KEY_RETURN = 10
ESC = 27
QUIT = {113, 81}  # Q)uit (ascii for upper & lower case Q/q)

# The following are globals:
highlight = 0
cmd_name = ''
ncmd_name = -1  # cmd_names[ncmd_name] == the current command
invalid_choice = False  
aborting = False
max_description_length = 0

cmds = {
        'ck_data': u.ck_data_cmd,
        'payables': u.payables_cmd,
        'show': u.show_cmd,
        'report': u.report_cmd,
        'stati': u.stati_cmd,
        }
cmd_names = sorted(cmds.keys())
ncmd_names = len(cmd_names)

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
        'stati': ('-D', '-M', '-B', '-s', '--mode', '-i', '-A', '-S', '-o', ),
            # -D -M -B -s stati --mode <mode> -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>
        }


def parse4usage(filename):
    """
    Parses the 'Usage:' part of utils.py.
    Returns a dict keyed by command.
    Each value is a listing of the possible options for that command.
    """
    ret = {}
    cmd = ''
    options = []
    parse = False
    with open(filename, 'r') as source:
        for line in source:
            line = line.strip()
            if line.startswith("Usage:"):
                parse = True
            elif parse:
                if not line:
                    break
                words = line.split()
                words = words[1:]  # get rid of "./utils.py"
                if (words[0] == '[-O]') or (
                    words[0].startswith('(label')):
                    # no command specified  DEBUG   # Simplify by
                    # or multi command possibility  # ignoring these
#                   print("ignoring: '{}'".format(line))
                    continue
                key = words[0]
                options = []
                for word in words[1:]:
                    if word.startswith(('[','(')):
                        word = word[1:]
                    if word.endswith((']',')')):
                        word = word[:-1]
                    if word.startswith('-'):
                        options.append(word)
                ret[key] = options
    return ret


def parse4options(filename):
    """
    Parses the 'Options:' part of utils.py.
    Returns a dict keyed by option. If both long and short options
    are provided they each have their (identical) entry.
    Each value is a list of strings (which can be '\n\t'.joined.)
    """
    global max_description_length
    ret = {}
    short_long = []
    text = []
    parse = False
    with open(filename, 'r') as source:
        for line in source:
            line = line.strip()
            if line.startswith("Options:"):
                # begin parsing next line
                parse = True
            elif parse:
                if not line:
                    # a blank line after parsing begins 
                    # means end of part needing parsing
                    break
                if line.startswith('-'):
                    # begin parsing a new option...
                    # but 1st save any data already collected:
                    if short_long:  # False when dealing /w 1st option
                        for key in short_long:
                            # if both long and short options
                            # we make an entry for each:
                            ret[key] = text  # Data collection
                            # we may not need the following global:
                            if len(text) > max_description_length:
                                max_description_length = len(text)
                        short_long = []
                        text = []
                    words = []  # collector for non arg part of line
                    for word in line.split():
                        if word.startswith('-'):
                            short_long.append(word)
                        else:
                            words.append(word)
                    text.append(' '.join(words))
                else:
                    text.append(line)
    return ret


def strip_leading_dashes(s):
    return s.lstrip('-')


explanations = parse4options('utils.py')
set_of_explanation_keys = set(explanations.keys())
ordered_explanation_keys = sorted(
        set_of_explanation_keys, key=strip_leading_dashes)
usage = parse4usage('utils.py')
set_of_usage_keys = set(usage.keys())
ordered_usage_keys = sorted(set_of_usage_keys)

#option_set = set(explanations.keys())
#options_ordered = sorted(option_set, key=strip_leading_dashes)
# for key in ordered_explanation_keys:
# for key in ordered_usage_keys:
#   print("% {}:  {}".format(key,
#               ', '.join(usage[key])))
# sys.exit()


def description(option, scr):
    """
    """
    if option in set_of_explanation_keys:
        text = []
        text.append("%{}:  {}".format(
            option, src[option][0]))
        text.extend(src[1:])
        return text
    else:
        return(["No description available for '{}'".format(option)])


def show_description(scr, description):
    opt_descript_window = cur.newwin
    pass

OPT_WIN_Y = 7
OPT_WIN_X = 2
OPT_DESCRIPT_Y = 12
OPT_DESCRIPT_X = 2

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


def option_keys(cmd):
    return(options[cmd])


def option_dict(cmd):
    """
    Provides a dict version.
    (See <option_listing> above.)
    """
    ret = {}
    for item in options[cmd]:
        ret[item] = u.args[item]
    return ret


def get_noptions(cmd):
    return len(options[cmd])


def print_menu(m_win, choices, hlight):
    x = y = 2
    m_win.box()
    m_win.addstr(1,x,
    "Up & Down arrows to select, <enter> to edit, <esc> when done: ",
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


def tofrotext(option):
    """
    None|True|False to/from text
    """
    if option == "None":
        return  None
    if option == "False":
        return  False
    if option == "True":
        return  True
    if option == None:
        return "None"
    if option == False:
        return  "False"
    if option == True:
        return  "True"
    assert isinstance(option, str)
    return option


def edited_option(scr, option, y):
    """
    Provides the editing capability:
    Returns the edited (or not) version of option.
    Editing window begins on line <y> of the <scr>een.
    """
    option = tofrotext(option)
    scr.addstr(y,0, "Edit the text then Ctrl-G to exit",
               cur.A_BOLD)
    scr.refresh()
    # create the text box with border around the outside
    tb_border = cur.newwin(3,52,y+1,9)
    tb_border.box()
    tb_border.refresh()
    tb_body = cur.newwin(1,50,y+2,10)
    tb = Textbox(tb_body)
    for ch in option:  # insert starting text
        tb.do_command(ch)
    tb.edit()  # start the editor running, Ctrl-G ends
    s2 = tb.gather()  # fetch the contents
    scr.clear()  # clear the screen
    return tofrotext(s2)


def get_chosen_cmd_index(scr):
    """
    Provides user with a listing of commands from which to choose.
    Returns the chosen command's index (into <cmd_names>.)  
    """
    scr.clear()
    maxy, maxx = scr.getmaxyx()

    # decide which command to execute:
    scr.addstr(0,0,
               "Welcome to the Bolinas Rod & Boat Club Utilities",
               cur.A_REVERSE)
    scr.addstr(1,0, "Available commands are as follows:", cur.A_BOLD)
    # present user with a listing of commands available...
    for n, cmd_name in enumerate(cmd_names, 1):
        scr.addstr(n+1, 4, 
                   "{}: {}".format(n, cmd_name))
    scr.addstr(2+ncmd_names,0, 'Choose command #: ', cur.A_BOLD)
    while True:
        c = scr.getch()
        scr.addstr(cur.LINES-4,10, "{}".format(c))
        scr.refresh()
        try:
            ncmd_name = int(chr(c))-1  ## WHAT if non integer?  DEBUG
        except ValueError:
            scr.addstr(2+ncmd_names,0,
                       'Must choose an integer between 1 and {}: '
                       .format(ncmd_names),
                       cur.A_BOLD)
            invalid_choice = True
            scr.clrtoeol()
            scr.refresh()
        else:
            if ((ncmd_name >= 0)            # }  valid
            and (ncmd_name < ncmd_names)):  # }  choice
                scr.addstr(2+ncmd_names,0, '    ')
                scr.clrtoeol()
                invalid_choice = False
                break
            else:
                scr.addstr(2+ncmd_names,0,
                           'Invalid choice- integer out of range: ',
                           cur.A_BOLD)
                scr.clrtoeol()
                scr.refresh()
                invalid_choice = True
        scr.addstr(cur.LINES-4,10, "{}".format(c))
    return ncmd_name


def main(scr):
    global highlight
    global cmd_name
    global ncmd_name
    global invalid_choice
    global aborting
    global max_description_length

    maxy, maxx = scr.getmaxyx()
    cmd_name = cmd_names[get_chosen_cmd_index(scr)]
    # we've established which command to run (so set up for it...)
    cmd_func = cmds[cmd_name]
    n_options = get_noptions(cmd_name)
    # initialize option changing application data:
    opt_win = cur.newwin(n_options+3, maxx,
                         4+ncmd_names,0)
    opt_win.keypad(True)
    highlight = 1
    choice = 1
    announcement = "Character last pressed: "
    scr.addstr(cur.LINES-5,0, announcement)
    scr.clrtoeol()
    scr.refresh()

    # event loop:
    while True:
        # Notify user of choice made:
        scr.addstr(2+ncmd_names, 0,
                   "You've chosen to execute '{}' command ..."
                   .format(cmd_name))
        scr.clrtoeol()
        scr.addstr(3+ncmd_names, 0,
                   "...but first select, edit & confirm options:")
        scr.refresh()

        cur.curs_set(0)
        print_menu(opt_win, option_listing(cmd_name),
                   highlight)
        c = opt_win.getch()
        cur.curs_set(1)
        scr.addstr(cur.LINES-4,10, "{}".format(c))
        scr.refresh()
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
            choice = highlight  # <choice> has been made
            scr.addstr(cur.LINES-2,0,
                    "Edit option %d. %s\n"%(choice, 
                    option_listing(cmd_name)[choice-1]))
            scr.clrtoeol()
            # Edit the chosen option here
            chosen_option = u.args[option_keys(cmd_name)[choice-1]]
            scr.addstr(cur.LINES-5,0, "Option to edit is: {}"
                    .format(str(chosen_option)))
#           scr.getch()
#           cur.curs_set(1)
            y_off_set = 8 + ncmd_names + n_options
            scr.addstr(y_off_set, 0,
                    "Editing command '{}' options..."
                    .format(cmd_name))
            revised_option = edited_option(scr,
                    chosen_option,
                    y_off_set + 1)
            u.args[option_keys(cmd_name)[choice-1]] = revised_option
#           cur.curs_set(0)
#           scr.getch()
            scr.addstr(cur.LINES-4,10, "{}".format(revised_option))
            scr.refresh()
        elif c == ESC:  # escape character
            scr.addstr(cur.LINES-1,0,
               "Finished editing options!! (any key to continue)")
            scr.clrtoeol()
#           scr.getch()
            scr.addstr(cur.LINES-4,10, "{}".format(c))
            scr.refresh()
            break
        scr.refresh()

    y_below_menu = 8+ncmd_names+get_noptions(cmd_name)
    scr.addstr(y_below_menu, 0,
               "About to execute '{}' command...."
               .format(cmd_name))
    scr.addstr(1+y_below_menu, 0,
               "<Esc> to abort or any other key to continue ... ")
#   cur.curs_set(1)
    scr.clrtoeol(); c = scr.getch()
    scr.addstr(cur.LINES-4,10, "{}".format(c))
    scr.refresh()
    if not c == ESC:
        cmd_func()
    else:
        aborting = True

cur.wrapper(main)

# outside of curses reporting:
print("Finished with 'curses interface'.")
if invalid_choice:
    print("Your choice ({}) is out of range.".format(ncmd_name))
elif aborting:
    print("Aborted running '{}' command".format(cmd_name))
else:
    print("Ran '{}' command".format(cmd_name))
