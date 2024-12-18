import numpy

from Modules.GenericPuzzle import MapPuzzle
from Modules.ReadFiles import read_file_as_char_map

''' custom sign function return 1 if 0 or positive otherwise return -1'''
def sign(number):
    if number < 0:
        return -1
    else:
        return 1

# scan the given slice and return the closest position for the given character
def scan_line(input_line, char):
    occlusions = numpy.where(input_line == char)[0]
    if len(occlusions) == 0: # no occlusions walk the full length
        return len(input_line)
    else:
        return min(occlusions)
''' Guard class is responsible for storing 
-location on the map
-direction facing on the map 

Guard is able to identify where on the map it is safe to move but cannot alter the map.'''
class Guard:
    def __init__(self, location, direction):
        self.location = location
        self.direction = direction

    # function to turn the guard direction
    def turn_guard_clockwise(self):
        match self.direction:
            case MapPuzzle.UP:
                self.direction = MapPuzzle.RIGHT
                return
            case MapPuzzle.RIGHT:
                self.direction = MapPuzzle.DOWN
                return
            case MapPuzzle.DOWN:
                self.direction = MapPuzzle.LEFT
                return
            case MapPuzzle.LEFT:
                self.direction = MapPuzzle.UP
                return

    '''This function will move the guard in a straight line until the first occlusion is hit,
    then turn the guard.
    
    Return the locations on the map the guard has walked.'''
    def move_to_next_turn(self, input_map):
        if self.direction == MapPuzzle.LEFT or self.direction == MapPuzzle.RIGHT:
            occ_ind = scan_line(input_map[self.location[0], self.location[1]::self.direction[1]], '#')
            cols = numpy.arange(self.location[1], self.location[1]+self.direction[1]*occ_ind, sign(self.direction[1]))
            rows = [self.location[0]]
        else:
            occ_ind = scan_line(input_map[self.location[0]::self.direction[0], self.location[1]],'#')
            rows = numpy.arange(self.location[0], self.location[0]+self.direction[0]*occ_ind, sign(self.direction[0]))
            cols = [self.location[1]]

        self.location = [rows[-1], cols[-1]]
        self.turn_guard_clockwise()
        return rows, cols

class PuzzleDay6(MapPuzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.guard = None
        self.map_size = numpy.array([0,0])

    def read_file(self):
        self.input = numpy.array(read_file_as_char_map(self.filename))
        self.map_size = numpy.array([self.input.shape[0] - 1, self.input.shape[1] - 1])

    # find the location and the direction the guard is facing
    # and put into our guard
    def find_guard(self):
        pos = self.find_start(self.input, '^')
        if pos:  # facing up
            self.guard = Guard(pos, self.UP)
            return
        pos = self.find_start(self.input, 'v')
        if pos:  # facing up
            self.guard = Guard(pos, self.DOWN)
            return
        pos = self.find_start(self.input, '<')
        if pos:  # facing up
            self.guard = Guard(pos, self.LEFT)
            return
        pos = self.find_start(self.input, '>')
        if pos:  # facing up
            self.guard = Guard(pos, self.RIGHT)


    # input_map is a 2D numpy array where # indicate obstacles
    # start_pos is a 2D numpy array where:
    #   -the first row indicates the 2D position of the guard in the array
    #   - the second row indicates the direction of movement
    def fill_in_next_line(self):
        rows, cols = self.guard.move_to_next_turn(self.input)
        self.input[rows, cols] = 'X'

    def part1(self):
        # first find where the guard is
        self.find_guard()

        # start by filling in the first line
        self.fill_in_next_line()

        # while the guard is not on the map boundary
        while not (numpy.any(self.guard.location == numpy.array([0, 0])) or numpy.any(self.guard.location == self.map_size)):
            # fill in the next line
            self.fill_in_next_line()

        # count X in the map
        return numpy.count_nonzero(self.input == 'X')


    def part2(self):
        pass