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
    # don't move forward if there's 'backlog'
    # all iterations end at State._A


input_file.close()
output_file.close()

sys.exit(0)
