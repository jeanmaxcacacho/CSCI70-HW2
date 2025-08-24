import sys
import io
from enum import Enum

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
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

# enter start
_state = State._A
_buffer = ""
_char = None
_pushback_char = None

while _state not in (State.EOF, State.ERROR):
    # don't move forward if there's 'backlog'
    if _pushback_char is not None:
        _char = _pushback_char
        _pushback_char = None
    else:
        _char = input_file.read(1)

    # invalid transition
    _char_grp = gk(_char)
    if _char_grp not in t_table[_state]:
        _state = State.ERROR
        output_file.write("this transition wasn't accounted for")
        break

    next_state, emit, pushback = t_table[_state][_char_grp]

    if emit is not None:
        if emit == "NUM":
            output_file.write(f"{emit}     {_buffer}\n")
        else:
            output_file.write(
                f"{emit}     {_char if emit in ('PLUS', 'MINUS') else ''}"
            )
        _buffer = ""

    if pushback:
        _pushback_char = _char
    else:
        if _state == State._B and _char_grp == "numeric":
            _buffer += _char

    _state = next_state

if _state == State.ERROR:
    if _char != "" and _char is not None:
        output_file.write(f"Lexical Error reading character \"{_char}\"\n")
    else:
        output_file.write("Lexical Error but unknown character \n")

input_file.close()
output_file.close()

sys.exit(0)
