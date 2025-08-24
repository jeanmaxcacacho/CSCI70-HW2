import sys
import io
from enum import Enum

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <input_file>")
    sys.exit(1)


def gk(_char):  # get key to shove in to t_table
    if _char == "":
        return "EOF"
    elif _char.isnumeric():
        return "numeric"
    elif _char in ("=", "+", "-", ""):
        return _char
    elif _char.isspace():
        return "whitespace"
    else:
        return "other"


class State(Enum):  # system can only be any one of these states at a time
    # intermediate states
    _A = "whitespace"
    _B = "unterminated digit"
    _E = "single equals"

    # 'housekeeping' states
    EOF = "END"
    ERROR = "ERROR"

    # 'full' states
    PLUS = "PLUS"
    MINUS = "MINUS"
    ASSIGN = "ASSIGN"
    NUM = "NUM"


"""
general rules of DFA (mimic the graph):
- the only valid tokens are ("==", "+", "-", and [0-9])
- _state, _emit, _pushback = t_table[_state][gk(_char)] -> move current state to next
"""
t_table = {
    State._A: {  # starting state/reset point
        "EOF": (State.EOF, None, False),
        "other": (State.ERROR, None, False),
        "whitespace": (State._A, None, False),
        "numeric": (State._B, None, False),
        "=": (State._E, None, False),
        "+": (State.PLUS, None, False),
        "-": (State.MINUS, None, False),
    },
    State._B: {
        "EOF": (State.NUM, "NUM", False),
        "other": (State.NUM, "NUM", True),
        "whitespace": (State.NUM, "NUM", True),
        "numeric": (State._B, None, False),
        "=": (State.NUM, "NUM", True),
        "+": (State.NUM, "NUM", True),
        "-": (State.NUM, "NUM", True),
    },
    State._E: {
        "EOF": (State.ERROR, None, False),
        "other": (State.ERROR, None, False),
        "whitespace": (State.ERROR, None, False),
        "numeric": (State.ERROR, None, False),
        "=": (State.ASSIGN, "ASSIGN", False),
        "+": (State.ERROR, None, False),
        "-": (State.ERROR, None, False),
    },
    State.PLUS: {
        "EOF": (State._A, None, False),
        "other": (State._A, None, False),
        "whitespace": (State._A, None, False),
        "numeric": (State._A, None, False),
        "=": (State._A, None, False),
        "+": (State._A, None, False),
        "-": (State._A, None, False),
    },
    State.MINUS: {
        "EOF": (State._A, None, False),
        "other": (State._A, None, False),
        "whitespace": (State._A, None, False),
        "numeric": (State._A, None, False),
        "=": (State._A, None, False),
        "+": (State._A, None, False),
        "-": (State._A, None, False),
    },
    State.ASSIGN: {
        "EOF": (State._A, None, False),
        "other": (State._A, None, False),
        "whitespace": (State._A, None, False),
        "numeric": (State._A, None, False),
        "=": (State._A, None, False),
        "+": (State._A, None, False),
        "-": (State._A, None, False),
    },
    State.NUM: {
        "EOF": (State._A, None, False),
        "other": (State._A, None, False),
        "whitespace": (State._A, None, False),
        "numeric": (State._A, None, False),
        "=": (State._A, None, False),
        "+": (State._A, None, False),
        "-": (State._A, None, False),
    },
    State.ERROR: {  # if encounter either ERROR/EOF stay there forever
        "EOF": (State.ERROR, None, False),
        "other": (State.ERROR, None, False),
        "whitespace": (State.ERROR, None, False),
        "numeric": (State.ERROR, None, False),
        "=": (State.ERROR, None, False),
        "+": (State.ERROR, None, False),
        "-": (State.ERROR, None, False),
    },
    State.EOF: {
        "EOF": (State.EOF, None, False),
        "other": (State.EOF, None, False),
        "whitespace": (State.EOF, None, False),
        "numeric": (State.EOF, None, False),
        "=": (State.EOF, None, False),
        "+": (State.EOF, None, False),
        "-": (State.EOF, None, False),
    },
}

# TODO: program execution
input_file = io.open(sys.argv[1], "r")
output_file = io.open(sys.argv[2], "w")

_char = input_file.read(1)  # get first char

_buffer = ""  # instantiate char stream
_buffer += _char  # flush _buffer not _char into output_file

input_file.close()
output_file.close()

sys.exit(0)
