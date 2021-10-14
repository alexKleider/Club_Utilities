#!/usr/bin/env python3

# File: interface.py   The curses interface.

"""
Curses interface to the 'utils.py' utility.
"""

import sys
import curses as cur
from curses.textpad import Textbox
import utils as u

DEBUG = True  # set to False in production
DEBUG = False  # set to False in production
KEY_RETURN = 10
ESC = 27
QUIT = {113, 81}  # Q)uit (set of ascii for upper & lower case Q/q)
TOP_LINE = 2
ANNOUNCE_LEN = 2
OPT_WIN_Y = TOP_LINE + ANNOUNCE_LEN

# The following are globals:
class Gbls(object):

    instances = 0
    debug = DEBUG

    def __init__(self):
        self.instances += 1
        if self.instances > 1:
            raise(NotImplementedError,
                    "Only one set of globals allowed.")
        self.highlight = 0
        self.cmd_name = ''
        self.ncmd_name = -1
        self.invalid_choice = False  
        self.aborting = False

        self.cmds = { # functions keyed by cmd name
                'ck_data': u.ck_data_cmd,
                'payables': u.payables_cmd,
                'show': u.show_cmd,
                'report': u.report_cmd,
                'stati': u.stati_cmd,
                }
        self.cmd_names = sorted(self.cmds.keys())
        self.ncmd_names = len(self.cmd_names)
        # gbls.cmd_names[gbls.ncmd_name] is the current command

gbls = Gbls()


def debug(scr, msgs, prompt="... any key to continue", debug=DEBUG):
    """
    If debug is set to True: Writes <msgs> (a string or list
    of strings) to the bottom of the <scr>een.
    If <prompt> is not an empty string, it's appended to <msgs>.
    Does nothing if not debug.
    """
    if debug:
        if isinstance(msgs, str):
            msgs = [msgs]
        if prompt:
            msgs.append(prompt)
        l = len(msgs)
        y = gbls.maxy-l-1
        for line in msgs:
            scr.move(y, 0)
            scr.clrtoeol()
            scr.addstr(y, 0, line)
            y += 1
        return scr.getch()  # there's an implied refresh


def show(scr, lines, y=1, x=1, prompt=""):
    """
    Writes <lines> onto <scr> beginning at (y,x).
    If <prompt>, will wait for and return ord of next char pressed.
    """
    if isinstance(lines, str):
        lines = [lines]
    if prompt:
        lines.append(prompt)
    for line in lines:
        scr.move(y, x)
        scr.clrtoeol()
        scr.addstr(y, x, line)
        y += 1
    if prompt:
        return scr.getch()
    else:
        scr.refresh()
        return 


def parse4usage(filename):
    """
    Returns a dict keyed by command name.
    Each value is a listing of the possible options for that command.
    Gets its data by parsing the 'Usage:' part of <filename> which
    is expected to be "utils.py" (as a SPoL.)
    Saved into gbls.opts_by_cmd
    """
    ret = {}
    cmd = ''
    opts = []
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
                    # Simplify by ignoring these
                    continue
                key = words[0]
                opts = []
                for word in words[1:]:
                    if word.startswith(('[','(')):
                        word = word[1:]
                    if word.endswith((']',')')):
                        word = word[:-1]
                    if word.startswith('-'):
                        opts.append(word)
                ret[key] = opts
    return ret


def parse4opt_descriptors(filename, gbls):
    """
    Returns a dict keyed by option. If both long and short options
    are provided they each have their (identical) entry.
    Each value is a list of strings describing the option.
    (These can be '\n\t'.joined.)
    Gets its data by parsing the 'Options:' part of <filename> which
    is expected to be "utils.py" (as a SPoL.)
    """
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
                if not line:  # No need to parse further
                    break     # after a blank line.
                if line.startswith('-'):
                    # begin parsing a new option...
                    # but 1st save any data already collected:
                    if short_long:  # False when dealing /w 1st option
                        for key in short_long:
                            # if both long and short options
                            # we make an entry for each:
                            ret[key] = text  # Data collection
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


def description(option, gbls):
    """
    Returns a list of strings (which can be '\n'.join()ed)
    describing the specified option.
    """
    if option in gbls.set_of_opt_descriptor_keys:
        text = []
        text.append("%{}:  {}".format(
                    option, gbls.opt_descriptors[option][0]))
        text.extend(gbls.opt_descriptors[option][1:])
        return text
    else:
        return(["No description available for '{}'".format(option)])


def show_description(scr, description, y=25, x=2):
    max_line_len = 0
    for line in description:
        if len(line) > max_line_len:
            max_line_len = len(line)
    nlines = len(description)
    descr_border = cur.newwin(nlines+2,max_line_len+4, y,x)
    descr_border.box()
    descr_win = cur.newwin(nlines,max_line_len+2,y+1,x+1)
    maxy, maxx = scr.getmaxyx()    #DEBUG
    for n, line in enumerate(description):
        descr_win.addstr(n,1,line)
    descr_border.refresh()
    descr_win.refresh()



def options_w_values_listing(cmd, args, gbls):
    """
    Provides a list of strings showing the options and
    their current values for the specified command.
    Ordered as they appear in their respective tuples.
    (See <gbls.opts_by_cmd> above.)
    (<args> is imported from utils as u)
    """
    ret = []
    for item in gbls.opts_by_cmd[cmd]:
        ret.append("{}: {}".format(
                   item, args[item]))
    return ret


def print_menu(m_win, choices, hlight):
    """
    Displays a menu of options from which to choose.
    One of options (specified by <hlight>) is highlighted.
    """
    y = x = 2
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


def tofrotext(value):
    """
    None|True|False to/from text
    Solves problem of textual representation of Boolean or None.
    """
    if value == "None":
        return  None
    if value == "False":
        return  False
    if value == "True":
        return  True
    if value == None:
        return "None"
    if value == False:
        return  "False"
    if value == True:
        return  "True"
    assert isinstance(value, str)
    return value


def edited_option(scr, option, y=8,x=2):
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


def collect_show_return_ch(scr,row):
    column = 10
    c = scr.getch()
    scr.move(row,column)
    scr.clrtoeol()
    scr.addstr(row,column,"{}".format(c))
    scr.refresh()
    return c


def get_chosen_cmd_index(scr, gbls):
    """
    0. clears the screen
    1. provides header lines and
    2. a listing of commands from which to choose,
    3. collects & returns the chosen command's index
    (into <gbls.cmd_names>.)  
    """
    scr.clear()
    scr.addstr(0,0,
               "Welcome to the Bolinas Rod & Boat Club Utilities",
               cur.A_REVERSE)
    scr.addstr(1,0, "Available commands are as follows:", cur.A_BOLD)
    for n, cmd_name in enumerate(gbls.cmd_names, 1):
        scr.addstr(n+1, 4, 
                   "{}: {}".format(n, cmd_name))
    scr.addstr(2+gbls.ncmd_names,0, 'Choose command #: ', cur.A_BOLD)
    while True:
        c = collect_show_return_ch(scr,cur.LINES-4)
        try:
            gbls.ncmd_name = int(chr(c))-1
        except ValueError:  # not an integer
            scr.addstr(2+gbls.ncmd_names,0,
                       'Must choose an integer between 1 and {}: '
                       .format(gbls.ncmd_names),
                       cur.A_BOLD)
            gbls.invalid_choice = True
            scr.clrtoeol()
            scr.refresh()
        else:
            if ((gbls.ncmd_name >= 0)                 # }  valid
            and (gbls.ncmd_name < gbls.ncmd_names)):  # }  choice
                scr.addstr(2+gbls.ncmd_names,0, '    ')
                scr.clrtoeol()
                gbls.invalid_choice = False
                break
            else:
                scr.move(2+gbls.ncmd_names,0)
                scr.clrtoeol()
                scr.addstr(2+gbls.ncmd_names,0,
                           'Invalid choice- integer out of range: ',
                           cur.A_BOLD)
                scr.refresh()
                gbls.invalid_choice = True
    scr.clear(); scr.refresh()
    return gbls.ncmd_name


gbls.opt_descriptors = parse4opt_descriptors('utils.py', gbls)
gbls.set_of_opt_descriptor_keys = set(gbls.opt_descriptors.keys())
gbls.ordered_opt_descriptor_keys = sorted(
        gbls.set_of_opt_descriptor_keys,
        key=lambda s: s.lstrip('-'))

gbls.opts_by_cmd = parse4usage('utils.py')
gbls.set_of_option_listings_by_cmd_name_keys = set(
        gbls.opts_by_cmd.keys())
gbls.ordered_option_listings_by_cmd_name_keys = sorted(
        gbls.set_of_option_listings_by_cmd_name_keys)


def main(scr):
    global gbls 
    gbls.maxy, gbls.maxx = scr.getmaxyx()
    ord_cmd = get_chosen_cmd_index(scr,gbls)
    gbls.cmd_name = gbls.cmd_names[ord_cmd]
    # we've established which command to run (so set up for it...)
    n_opts = len(gbls.opts_by_cmd[gbls.cmd_name])
    # initialize option changing application data:
    opt_win = cur.newwin(n_opts+3, gbls.maxx,
                         OPT_WIN_Y,0)
    opt_win.keypad(True)
    gbls.highlight = 1
    choice = 1
    show(scr, ["You've chosen to execute '{}' command ..."
                .format(gbls.cmd_name),
               "...but first select, edit & confirm options:",
               ], 2, 0)

    # event loop:
    while True:
        cur.curs_set(0)
        print_menu(opt_win,
                   options_w_values_listing(gbls.cmd_name,
                                            u.args, gbls),
                   gbls.highlight)
        c = opt_win.getch()
        cur.curs_set(1)
        debug(scr, ["Ord of key pressed: '{}'.".format(c),])
        cy, cx = opt_win.getyx()
        if c == cur.KEY_UP:
            if gbls.highlight == 1:
                gbls.highlight = n_opts  # move hl to bottom
                opt_win.move(n_opts,0)
            else: gbls.highlight -= 1
            opt_win.move(gbls.highlight,0)
        elif c == cur.KEY_DOWN:
            if gbls.highlight == n_opts:
                gbls.highlight = 1  # move hl to top
                opt_win.move(gbls.highlight,0)
            else: gbls.highlight += 1
            opt_win.move(gbls.highlight,0)
        elif c in (KEY_RETURN, cur.KEY_ENTER):
            ord_opt = gbls.highlight  # ordinal of option to edit
            option_w_value = (
                    options_w_values_listing(gbls.cmd_name,
                                             u.args,
                                             gbls)[ord_opt-1])
            option = option_w_value.split(':')[0]
            option_value = option_w_value.split(':')[1].strip()
            y_offset = OPT_WIN_Y + n_opts + 3
            show(scr,
                ["Edit option %s (description follows)"%(option_w_value),],
                y = y_offset)
            # Edit the chosen option here
            debug(scr, ["index is '{}'".format(ord_opt-1),
                        "gbls.cmd_name is '{}'"
                            .format(repr(gbls.cmd_name)),
                        "index is '{}'".format(gbls.opts_by_cmd[
                            gbls.cmd_name][ord_opt-1]),
                            ])
            chosen_option_value = u.args[
                    gbls.opts_by_cmd[gbls.cmd_name][ord_opt-1]
                    ]
            opt_descript = description(option, gbls)
            y_offset += 1
            show_description(scr,
                    opt_descript,
                    y_offset, 0)
            debug(scr, ["Option to edit is: {}"
                    .format(str(chosen_option_value)),])
            y_offset += len(opt_descript) + 2
            revised_option = edited_option(scr,
                    chosen_option_value,
                    y_offset)
            debug(scr,[name for name in gbls.cmd_names])
            debug(scr,str(ord_cmd-1))
            debug(scr,[opt for opt in gbls.opts_by_cmd['stati']])
            u.args[gbls.opts_by_cmd[
                gbls.cmd_name][ord_opt-1]] = revised_option
            y_offset += 2
            scr.addstr(y_offset,0, "{}".format(revised_option))
            scr.clrtoeol()
            scr.refresh()
        elif c == ESC:  # escape character
            scr.clear()
            ch = show(scr, 
               ["Finished editing options!!",
                "About to execute '{}' command."
                .format(gbls.cmd_name)],
               OPT_WIN_Y, 0,
               "<Esc> to abort or any other key to continue ... ")
            break

    if ch == ESC:
        gbls.aborting = True

cur.wrapper(main)

# outside of curses reporting:
print("Finished with 'curses interface'.")
if gbls.invalid_choice:
    print("Your choice ({}) is out of range.".format(ngbls.cmd_name))
elif gbls.aborting:
    print("Aborted running '{}' command".format(gbls.cmd_name))
else:
    print("Running '{}' command".format(gbls.cmd_name))
    gbls.cmds[gbls.cmd_name]()
