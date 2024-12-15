from functools import cache
from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

def splint_int(number):
    str_num = str(number)
    split_ind = len(str(str_num)) // 2
    return int(str_num[0:split_ind]), int(str_num[split_ind::])

@cache
def blink(item, step):
    if step == 0:
        return 1

    # increment by one
    if item == 0:
        return blink(1, step - 1)
    # split in two
    elif len(str(item)) % 2 == 0:
        num1, num2 = splint_int(item)
        counter = blink(num1, step - 1)
        counter += blink(num2, step - 1)
        return counter

    return blink(item * 2024, step - 1)

class PuzzleDay11(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        self.input = ReadFiles.read_file_as_int_list(self.filename)[0]

    def part1(self):
        counter = 0
        for x in self.input:
            counter += blink(x, 25)
        return counter

    def part2(self):
        counter = 0
        for x in self.input:
            counter += blink(x, 75)
        return counter