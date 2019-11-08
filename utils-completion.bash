#!/usr/bin/env bash

# File: utils-completion.bash
# ... a completion script for utils.py
# To be effective, this script must be "sourced". This can be done
# automatically by adding
# "source <path-to-script>/utils-completion.bash"
# as a single line to ~/.profile in your home directory.
#

complete -W "ck_fields \
            show \
            stati \
" utils.py

# defines a completion specification (compspec) for a program..
# ..in this case the program is 'utils.py'
# ..and we use the -W (wordlist) option.
# <complete> is a Bash builtin.

