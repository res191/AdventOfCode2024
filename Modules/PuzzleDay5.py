import numpy

from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

# return 0 if you get to the end of the file and have not swapped anything
# otherwise return the index of the first item swapped
def swap_incorrect_match(input_line, rulebook, startInd):
    for i in range(startInd, 0, -1):
        rules_to_check = rulebook[rulebook[:,0]==input_line[i],1]
        for j in range(0, i):
            if numpy.any(rules_to_check==input_line[j]):
                # swap the two elements
                input_line[i], input_line[j] = input_line[j], input_line[i]
                return i
    return 0

# return false when a rule is broken
# if you make it to the end of the line without violating any rules return true
def validate_line(input_line, rulebook):
    for i in range(len(input_line) - 1, 0, -1):
        rules_to_check = rulebook[rulebook[:, 0] == input_line[i], 1]
        for rule in rules_to_check:
            if numpy.any(input_line[0:i] == rule):
                return False
    return True

class PuzzleDay5(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.rulebook = None

    def read_file(self):
        file_output = ReadFiles.read_file_as_list(self.filename)

        # split the output into the rulebook and the input
        index = file_output.index('')
        self.rulebook = numpy.array([list(map(int, line.split('|'))) for line in file_output[:index - 1]])
        self.input = [list(map(int, line.split(','))) for line in file_output[index + 1:]]


    def part1(self):
        count = 0
        for item in self.input:
            if validate_line(numpy.array(item), self.rulebook):
                count += item[(len(item) - 1) // 2]
        return count

    def part2(self):
        count = 0

        for item in self.input:
            input_arr = numpy.array(item)
            swap_ind = swap_incorrect_match(input_arr, self.rulebook, len(input_arr) - 1)

            while swap_incorrect_match(input_arr, self.rulebook, swap_ind) != 0:
                continue

            if swap_ind > 0:
                count += input_arr[(len(item) - 1) // 2]
        return count