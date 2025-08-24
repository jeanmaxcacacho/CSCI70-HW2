"""
general rules of DFA (from the graph):
- starting state is any whitespace/empty character
- alphabetic characters are not part of any valid tokens
- the only valid tokens are ("==", "+", "-", and [0-9])

general notes for program
- read the file character by character
- write buffers to file not characters, flush per transition

let's rigorously define pushback behaviour
- if transitioning out of NUM to a valid state, flush current buffer contents
- then append current character to the current buffer, "reread" current char
"""

import sys
import io
from enum import Enum

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)


class State(Enum):  # system can only be any one of these states at a time
    BLANK = "BLANK"
    ERROR = "ERROR"
    NUM = "NUM"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EOF = "EOF"


def gk(c):  # get key to shove in to t_table
    if c.isnumeric():
        return "numeric"
    elif c in ("=", "+", "-", ""):
        return c
    elif c.isspace():
        return "blank"
    else:
        return "other"


# TODO: fix _token: double check t_table
# t_table[state][char] -> (_state, _token, _pushback)
# _state: following state, _token: token ID of char, _pushback: pushback bool
t_table = {
    State.BLANK: {  # catch-all state
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, None, False),
        "-": (State.MINUS, None, False),
        "numeric": (State.NUM, None, False),
        "": (State.EOF, None, False),
    },
    State.NUM: {  # digits accumulate, shifts to other states cut that number
        "blank": (State.BLANK, "NUM", False),
        "other": (State.ERROR, "NUM", False),
        "=": (State.BLANK, "NUM", True),  # blank state to account for pushback
        "+": (State.BLANK, "NUM", True),
        "-": (State.BLANK, "NUM", True),
        "numeric": (State.NUM, None, False),  # keep accumulating
        "": (State.EOF, "NUM", False),
    },
    State.ASSIGN: {  # already have first '=', only valid is another '='
        "blank": (State.ERROR, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.BLANK, "ASSIGN", False),  # only at second '='
        "+": (State.ERROR, None, False),
        "-": (State.ERROR, None, False),
        "numeric": (State.ERROR, None, False),
        "": (State.ERROR, None, False),
    },
    State.PLUS: {  # '+' and '-' can be in series, same transition rules
        "blank": (State.BLANK, "PLUS", False),
        "other": (State.ERROR, "PLUS", False),
        "=": (State.ASSIGN, "PLUS", False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "PLUS", False),
        "numeric": (State.NUM, "PLUS", False),
        "": (State.EOF, "PLUS", False),
    },
    State.MINUS: {
        "blank": (State.BLANK, "MINUS", False),
        "other": (State.ERROR, "MINUS", False),
        "=": (State.ASSIGN, "MINUS", False),
        "+": (State.PLUS, "MINUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "MINUS", False),
        "": (State.EOF, "MINUS", False),
    },
    State.ERROR: {  # ERROR and EOF only have debug transitions
        "blank": ("KEY 'blank' WENT TO ERROR", "NO EMIT", None),
        "other": ("KEY 'other' WENT TO ERROR", "NO EMIT", None),
        "=": ("KEY '=' WENT TO ERROR", "NO EMIT", None),
        "+": ("KEY '+' WENT TO ERROR", "NO EMIT", None),
        "-": ("KEY '-' WENT TO ERROR", "NO EMIT", None),
        "numeric": ("KEY 'numeric' WENT TO ERROR", "NO EMIT", None),
        "": ("KEY '' WENT TO ERROR", "NO EMIT", None),
    },
    State.EOF: {
        "blank": ("KEY 'blank' WENT TO EOF", "NO EMIT", None),
        "other": ("KEY 'other' WENT TO EOF", "NO EMIT", None),
        "=": ("KEY '=' WENT TO EOF", "NO EMIT", None),
        "+": ("KEY '+' WENT TO EOF", "NO EMIT", None),
        "-": ("KEY '-' WENT TO EOF", "NO EMIT", None),
        "numeric": ("KEY 'numeric' WENT TO EOF", "NO EMIT", None),
        "": ("KEY '' WENT TO EOF", "NO EMIT", None),
    }
}

"""
1. open IO streams
2. instantiate 1st character states
3. enter main driver loop

remember that we want to to flush the buffer not the
character into output_file

writing to output_file cases:
(i) any state (that's not NUM and ASSIGN) transition
(ii) for same state transitions only flush '+' and '-'
(iii) for '=', we only flush that in twos, else, error
(iv) NUM only gets flushed when we exit out of the NUM state

_buffer format
f'{_emit}   {_buffer}'
"""

# TODO: program execution
input_file = io.open(sys.argv[1], "r")
output_file = io.open(sys.argv[2], "w")

_char = input_file.read(1)  # get first char

_buffer = ""  # instantiate char stream
_buffer += _char  # flush the buffer not the char into output_file

_state, _emit, _pushback = t_table[State.BLANK][gk(_char)]  # enter first state


# while current_state != State.EOF:
#     # read a character, assign current_character
#     current_character = input_file.read(1)
#     # print(f"{current_character} | | {current_state}")
#
#     # transition state via t_table, this also handles EOF
#     _state, _token, _pushback = t_table[current_state][gk(current_character)]
#     current_state = _state
#
#     # only the ff: go forward
#     # State.BLANK, State.NUM, State.PLUS, State.MINUS and State.EOF
#     output_file.write(f"{_token} | {current_character}\n")

# program egress
if _state == State.ERROR:
    print(f"Lexical Error reading character \"{_char}\"")

# close io streams since we're good software engineers
input_file.close()
output_file.close()

sys.exit(0)
