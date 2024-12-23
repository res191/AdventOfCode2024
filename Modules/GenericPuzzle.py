import time
import numpy

''' custom sign function return 1 if 0 or positive otherwise return -1'''
def sign(number):
    if number < 0:
        return -1
    else:
        return 1

''' The most generic puzzle class. It requires derived classes to implmenent 
-read_file to set self.input appropriately
-part1 to solve part1 of the puzzle and return the correct value
-part2 to sove part2 of the puzzle and return the correct value
-implements solve function with a time to display the puzzle answer and time take on compute'''
class Puzzle:
    # the puzzle takes as input a filename
    def __init__(self, filename):
        self.filename = filename
        self.input = None

    # this file must set self.input using information from self.filename
    def read_file(self):
        raise NotImplementedError("Must override read_file")

    # run the solution to puzzle part 1
    def part1(self):
        raise NotImplementedError("Must override part1")

    # run the solution to puzzle part 2
    def part2(self):
        raise NotImplementedError("Must override part2")

    def solve(self):
        self.read_file()

        start_part1 = time.time()
        print('Solution to part 1 is: ', self.part1())
        end_part1 = time.time()
        print('Taking ', end_part1 - start_part1)

        start_part2 = time.time()
        print('Solution to part 2 is: ',  self.part2())
        end_part2 = time.time()
        print('Taking ', end_part2 - start_part2)

''' A puzzle for help with navigating maps. 
-It hard codes direction definitions
-Implements a check for finding the starting location for a given character in a map assuming the map 
is a numpy array. '''
class MapPuzzle(Puzzle):

    UP    = [-1, 0]
    DOWN  = [1, 0]
    LEFT  = [0, -1]
    RIGHT = [0, 1]

    DIRECTIONS=[UP, DOWN, LEFT, RIGHT]

    ''' Return the location of val if and only if there is one unique position on the map'''
    def find_start(self, input_map, val):
        pos = numpy.argwhere(input_map == val)
        if len(pos)> 1:
            print("Multiple starting positions detected this should never happen!")
        elif len(pos) == 0:
            return None
        return pos[0]

    ''' return true if the position is a valid for the given map'''
    def position_in_bounds(self, input_map, position):
        return numpy.all(position < input_map.shape) and numpy.all(position > -1)
