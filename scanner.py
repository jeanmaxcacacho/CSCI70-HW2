"""
general rules of DFA (from the graph):
- starting state is any whitespace/empty character
- alphabetic characters are not part of any valid tokens
- the only valid tokens are ("==", "+", "-", and [0-9])

general notes for program
- read the file character by character
- write buffers to file not characters, flush per transition
"""

import sys
import io
from enum import Enum

if len(sys.argv) != 2:
    print(f"[ERROR] Usage: python {sys.argv[0]} <input_file>")
    sys.exit(1)


class State(Enum):  # system can only be any one of these states at a time
    BLANK = "BLANK"
    ERROR = "ERROR"
    NUM = "NUM"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EOF = "EOF"


def group_char(c):  # utility function to get character key
    if c.isnumeric():
        return "numeric"
    elif c in ("=", "+", "-"):
        return c
    elif c.isspace():
        return "blank"
    else:
        return "other"


# transitions[current_state][char] -> (next_state, emit_token, need_pushback)
t_table = {
    State.BLANK: {
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "NUM", False),
    },
    State.NUM: {  # digit keep continuing, but if not then go back
        "blank": (State.BLANK, "NUM", False),  # ignore whitespace
        "other": (State.ERROR, None, False),
        "": (State.EOF, "NUM", False),
        "=": (State.ASSIGN, None, True),
        "+": (State.PLUS, "PLUS", True),
        "-": (State.MINUS, "MINUS", True),
        "numeric": (State.NUM, None, False),
    },
    State.ASSIGN: {
        "blank": (State.ERROR, None, False),
        "other": (State.ERROR, None, False),
        "": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, True),
        "+": (State.ERROR, None, True),
        "-": (State.ERROR, None, True),
        "numeric": (State.NUM, None, False),
    },
    State.PLUS: {  # digits can follow one after another
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "NUM", False),
    },
    State.MINUS: {
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "NUM", False),
    },
    State.ERROR: {},  # no transitions here
    State.EOF: {}  # no transitions here also
}


current_state = State.BLANK
current_buffer = ""
current_character = ""

input_file = io.open(sys.argv[1], "r")
# output_file = io.open("output.txt", "w")


# TODO: finish driver loop
while current_state not in (State.ERROR, State.EOF):
    # read a character, assign current_character
    current_character = input_file.read(1)
    if current_character == "":
        current_state = State.EOF
        break
    # do state transitions by invoking transition table
    _state, _token, _pushback = t_table[current_state][group_char(
        current_character)]
    current_state = _state  # transition to next state
    print(f"STATE: {current_state} CHAR: {current_character}")


# program egress
if current_state == State.ERROR:
    print(f"Lexical Error reading character \"{current_character}\"")

# close io streams since we're good software engineers
# input_file.close()
# output_file.close()

sys.exit(0)
