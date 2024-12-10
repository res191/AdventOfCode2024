import re
from Modules.GenericPuzzle import Puzzle
from Modules.ReadFiles import read_file_as_string

""" Compute the sum of the multiplication of each row in the a Nx2 list of integers.
"""
def compute_value(number_pairs):
    return sum(int(row[0]) * int(row[1]) for row in number_pairs)

def parse_line(input_line):
    muls = list()
    all_items = re.findall(r'mul\(\d{1,3},\d{1,3}\)', input_line)
    for item in all_items:
        muls.append(re.findall(r'\d{1,3}', item))
    return muls

class PuzzleDay3(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    """ Read the entire file as a single string
    """
    def read_file(self):
        self.input = "".join(read_file_as_string((self.filename)))

    def part1(self):
        return compute_value(parse_line(self.input))

    def part2(self):
        all_list = re.split('do\\(\\)',self.input)

        muls = list()
        for item in all_list:
            good_item = re.split("don\\'t\\(\\)", item, maxsplit=1)
            muls = muls + parse_line(good_item[0])

        return compute_value(muls)