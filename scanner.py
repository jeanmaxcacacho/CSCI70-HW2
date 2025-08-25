import sys
import io
from utils import gk, State, t_table

if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <input_file> <output_file>")
    sys.exit(1)

input_file = io.open(sys.argv[1], "r")
input_text = input_file.read()
input_file.close()

output_file = io.open(sys.argv[2], "w")

_state = State._A
_buffer = ""
position = 0
tokens = []

while _state not in [State.EOF, State.ERROR]:
    if position < len(input_text):
        _char = input_text[position]
    else:
        _char = ""  # EOF

    char_key = gk(_char)
    next_state, emit, pushback = t_table[_state][char_key]

    if not pushback:
        # normal character consumption
        if _state == State._A:
            if char_key == "numeric":
                _buffer = _char
            elif char_key in ("+", "-", "="):
                _buffer = _char
        # whitespace and terminal states don't need buffering
        elif _state == State._B and char_key == "numeric":
            _buffer += _char
        elif _state == State._E and char_key == "=":
            _buffer += _char

        position += 1

    if emit:
        tokens.append((emit, _buffer))
        _buffer = ""

    _state = next_state

# exit sequence
for token_type, token_value in tokens:
    # print(f"{token_type}\t{token_value}")
    output_file.write(f"{token_type}\t{token_value}\n")

# error egress
if _state == State.ERROR:
    # print(f"Lexical Error reading character \"{_char}\"")
    output_file.write(f"{token_type}\t{token_value}\n")
    sys.exit(1)

sys.exit(0)
