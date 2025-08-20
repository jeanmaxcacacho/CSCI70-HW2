"""
general rules of DFA (take get from the graph):
- starting state is any whitespace character
- alphabetic characters are not part of any valid tokens
- the only valid tokens are ("==", "+", "-", and [0-9])

general notes for program
- read the file character by character

why did it use my company email

"""

import sys
import io
import string  # string.isalpha(), string.isnum()
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


# TODO: finish tran table
# transitions[current_state][char] -> (next_state, emit_token, need_pushback)
transitions = {
    State.BLANK: {
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "NUM", False),
    },
    State.NUM: {  # TODO: this part of the tran table still isn't done
        "blank": (State.BLANK, "NUM", False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, ),
    },
    State.ASSIGN: {
        "other": (State.ERROR, None),  # anything else that isn't '='
        "=": (State.ASSIGN, "EQUALS"),
    },
    State.PLUS: {
        "blank": (State.BLANK, None, False),
        "other": (State.ERROR, None, False),
        "=": (State.ASSIGN, None, False),
        "+": (State.PLUS, "PLUS", False),
        "-": (State.MINUS, "MINUS", False),
        "numeric": (State.NUM, "NUM", False),
    },
    State.MINUS: {
        "blank": (State.BLANK, None),
        "other": (State.ERROR, None),
        "=": (State.ASSIGN, None),
        "+": (State.PLUS, "PLUS"),
        "-": (State.MINUS, "MINUS"),
        "numeric": (State.NUM, "NUM"),
    },
    State.ERROR: {},  # no transitions here
    State.EOF: {}  # no transitions here also
}


current_state = State.BLANK
need_pushback = False
current_buffer = ""
current_character = ""

input_file = io.open(sys.argv[1], "r")
output_file = io.open("output.txt", "w")

# TODO: finish driver loop
while current_state not in (State.ERROR, State.EOF):
    # read a character, assign currentCharacter
    currentCharacter = input_file.read(1)
    # if currentCharacter == "":
    #     currentState = State.EOF
    # write to buffer, if state transition happens flush buffer to output_file
    # output_file.write(currentCharacter)

input_file.close()
output_file.close()
sys.exit()
