
import numpy
import re
import matplotlib.pyplot as plt

from Modules.GenericPuzzle import Puzzle

col_size = 101
row_size = 103

def count_quadrant(col_pos, row_pos, quad):
    # for the upper left quadrant
    if quad == 1:
       return sum(row_pos[col_pos < col_size // 2] < row_size // 2)
    elif quad == 2:
        return sum(row_pos[col_pos > col_size // 2] < row_size // 2)
    elif quad == 3:
        return sum(row_pos[col_pos < col_size // 2] > row_size // 2)

    return sum(row_pos[col_pos > col_size // 2] > row_size // 2)


class PuzzleDay14(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        f = open(self.filename, "r")

        self.input = []
        for line in f.readlines():
            line = line.replace('p=','')
            line = line.replace('v=','')
            nums =  re.split(r',| ', line)
            self.input.append([int(num) for num in nums])

        f.close()

    def part1(self):
        input_array = numpy.array(self.input)

        new_col = input_array[:,0] + 100 * input_array[:,2]
        new_row = input_array[:,1] + 100 * input_array[:,3]

        new_col = new_col % col_size
        new_row = new_row % row_size

        safety_factor = 1
        for i in range(1,5):
            safety_factor *= count_quadrant(new_col, new_row, i)

        return safety_factor


    def part2(self):
        input_array = numpy.array(self.input)

        for i in range(0, 10000):
            new_col = input_array[:, 0] + i * input_array[:, 2]
            new_row = input_array[:, 1] + i * input_array[:, 3]

            new_col = new_col % col_size
            new_row = new_row % row_size

            input_map = numpy.zeros([row_size, col_size])
            for row, col in zip(new_row, new_col):
                input_map[row,col] += 1

            if numpy.max(input_map[:]) == 1:
                plt.imshow(input_map)
                plt.title('Seconds '+str(i))
                plt.show()
