from functools import cache
from Modules.GenericPuzzle import  Puzzle
from Modules.ReadFiles import read_file_as_list

@cache
def compute_moves(error_pos, input_code, position):
    control_list = []
    for request in input_code:
        # try to rank moves by preference < is farthest to A so it goes first, then v and finally ^ or >
        row_move = '^' if request[0] < position[0] else 'v'
        col_move = '<' if request[1] < position[1] else '>'

        row_first_error = request[0] == error_pos[0] and position[1] == error_pos[1]
        col_first_error = request[1] == error_pos[1] and position[0] == error_pos[0]

        # we should move column first if we are moving left
        # if an error is encounter if we move row first
        # or where moving column first adds spaces but does not cause an error
        if row_first_error or (col_move == '<' and not col_first_error):
            control_list += col_move * abs(request[1] - position[1]) + row_move * abs(request[0] - position[0]) + 'A'
        else:
            control_list += row_move * abs(request[0] - position[0]) + col_move * abs(request[1] - position[1]) + 'A'

        position = request

    return control_list

''' Robot base class to identify the moves given the requested key.'''
class Robot():
    def __init__(self):
        self.keypad      = None
        self.position    = None

    def request_moves(self, input_code):
        # iterator over each item
        control_list = []
        requests = []
        for elem in input_code:
            requests += [tuple(self.keypad[elem])]

            if elem == 'A':
                control_list += compute_moves(tuple(self.keypad['E']), tuple(requests), tuple(self.keypad['A']))
                requests= []

        return control_list

class DirectionPad(Robot):
    def __init__(self):
        super().__init__()
        self.keypad = { 'E': [0, 0], '^': [0, 1], 'A': [0, 2],
                        '<': [1, 0], 'v': [1, 1], '>': [1, 2]}
        self.position = self.keypad['A']

class NumberPad(Robot):
    def __init__(self):
        super().__init__()
        self.keypad = { '7': [0, 0], '8': [0, 1], '9': [0, 2],
                        '4': [1, 0], '5': [1, 1], '6': [1, 2],
                        '1': [2, 0], '2': [2, 1], '3': [2, 2],
                        'E': [3, 0], '0': [3, 1], 'A': [3, 2]}
        self.position = self.keypad['A']

class PuzzleDay21(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        self.input = read_file_as_list(self.filename)

    def part1(self):
        direction_pad2 = DirectionPad()
        direction_pad1 = DirectionPad()
        number_pad = NumberPad()

        count = 0
        for code in self.input:
            keystrokes = number_pad.request_moves(code)
            keystrokes = direction_pad1.request_moves(keystrokes)
            keystrokes = direction_pad2.request_moves(keystrokes)
            count += int(code[0:-1])*len(keystrokes)
        return count

    def part2(self):
        number_pad = NumberPad()
        robot_pad = DirectionPad()

        count = 0
        for code in self.input:
            keystrokes = number_pad.request_moves(code)

            for _ in range(26):
                keystrokes = robot_pad.request_moves(keystrokes)

            count += int(code[0:-1])*len(keystrokes)
        return count
