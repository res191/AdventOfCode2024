from lib2to3.fixer_util import find_root

import numpy

from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

class PuzzleDay15(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.map = None
        self.robot = None

    def read_file(self):
        file_output = ReadFiles.read_file_as_list(self.filename)

        index = file_output.index('')
        self.map = numpy.array([list(line) for line in file_output[0:index]])
        self.input = "".join(file_output[index+1::])

    def find_robot(self):
        pos = numpy.where(self.map == "@")
        if len(pos[0])> 1 or len(pos[1]) > 1:
            print("Multiple robots detected this should never happen!")

        self.robot = numpy.array([pos[0][0], pos[1][0]])

    # update the map based on the robot and the step
    def take_step(self, step):
        # figure out how many boxes we will push
        new_pos = self.robot+step

        # cannot take a step so return
        if self.map[new_pos[0], new_pos[1]] == '#':
            return
        # can take a step but there is a box in the way
        elif self.map[new_pos[0], new_pos[1]] == 'O':
            # we have a box at the next position
            # find the next element in the chain that is not a box
            if step[0] == 0:
                line_to_scan = self.map[new_pos[0], new_pos[1]::numpy.sign(step[1])]
            else:
                line_to_scan = self.map[new_pos[0]::numpy.sign(step[0]), new_pos[1]]

            next_empty_pos = numpy.where(line_to_scan =='.')[0]
            # we have no empty space so cannot move to the next step
            if len(next_empty_pos)== 0:
                return

            boxes = min(next_empty_pos)
            # we have a wall in the way
            if numpy.any(line_to_scan[:boxes]=='#'):
                return

            # otherwise move the boxes
            for i in range(0, boxes ):
                new_pos += step
                self.map[new_pos[0], new_pos[1]] = 'O'

        # move our robot and update the map
        self.map[self.robot[0],self.robot[1]] = '.'
        self.robot = self.robot+step
        self.map[self.robot[0],self .robot[1]] = '@'

    def part1(self):
        self.find_robot()

        for elem in self.input:
            if elem == "^":  # facing up
                self.take_step([-1, 0])
            if elem == "v":  # facing down
                self.take_step([1, 0])
            elif elem == ">":  # facing left
                self.take_step([0, 1])
            if elem == "<":  # facing right
                self.take_step([0, -1])
        box_pos = numpy.where(self.map=='O')
        count = 0
        for row, col in zip(box_pos[0], box_pos[1]):
            count+= row * 100 + col

        return count
    def part2(self):
        pass