import sys
import io

from utils import gk, State, t_table

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)

# TODO: program execution
input_file = io.open(sys.argv[1], "r")
output_file = io.open(sys.argv[2], "w")

# enter start
_state = State._A
_buffer = ""
_char = None
_pushback_char = None

while _state not in (State.EOF, State.ERROR):
    # cursor doesn't move if there's a pushback character
    if _pushback_char is not None:
        _char = _pushback_char
    else:
        _char = input_file.read(1)

    # a complete 'step' is a full cycle ending at State._A
    while _state != State._A:
        print("I bussed in my shorts!")

        # something something something.....

        next_state, emit_token, pushback = t_table[_state][gk(_char)]


input_file.close()
output_file.close()

sys.exit(0)
