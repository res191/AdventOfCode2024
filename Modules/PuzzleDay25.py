import numpy

from Modules.GenericPuzzle import Puzzle
from Modules.ReadFiles import read_file_as_char_map

class PuzzleDay25(Puzzle):
    def __init__(self):
        super().__init__()

    def read_file(self):
        self.input = read_file_as_char_map(self.filename)

    def part1(self):
        locks = []
        keys = []
        for i in range(0, len(self.input), 8):
            input_array = numpy.sum(numpy.array(self.input[i:i+7]) =='#', axis=0)
            # we are a lock
            if self.input[i][0] == '#':
                locks.extend([input_array])
            # we are a key
            elif self.input[i][0] == '.':
                keys.extend([input_array])

        locks = numpy.array(locks)
        keys = numpy.array(keys)

        count = 0
        for lock in locks:
            count+= sum(numpy.all(keys + numpy.ones([250,1])*[lock] < 8, axis=1))

    def part2(self):
        pass