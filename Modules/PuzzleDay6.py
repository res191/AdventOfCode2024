import numpy
from operator import add

from Modules.GenericPuzzle import MapPuzzle
from Modules.GenericPuzzle import sign
from Modules.ReadFiles import read_file_as_char_map
from Modules.TrackGuard import turn_guard_clockwise

''' scan the given slice and return the closest position for the given character '''
def scan_line(input_line, char):
    occlusions = numpy.where(input_line == char)[0]
    if len(occlusions) == 0: # no occlusions walk the full length
        return len(input_line)
    else:
        return min(occlusions)

''' detect if the guard is in a loop on the input_map'''
def is_in_loop(input_map, guard):
    cache_pos = []
    steps = 0

    map_size = numpy.array([input_map.shape[0] - 1, input_map.shape[1] - 1])
    # just to make sure we do not loop forever
    while steps < 5000:
        # if guard on map border return False
        if numpy.any(guard.location == 0) or numpy.any(guard.location == map_size):
            return False

        # if guard matches position return true
        curr_pos = [list(guard.location), guard.direction]
        for i in range(steps%4, len(cache_pos), 4):
            if cache_pos[i] == curr_pos:
                return True

        # if we are not yet in a loop or at the edge continue moving the guard
        cache_pos.append(curr_pos.copy())

        #move to the next obstacle
        guard.move_to_next_turn(input_map)
        steps += 1

    # Guard entered an undetected loop, this should never happen.
    # Print a message and return true when maximum steps reached.
    print('We have reached ', steps, '!')
    return False

''' Guard class is responsible for storing 
-location on the map
-direction facing on the map 

Guard is able to identify where on the map it is safe to move but cannot alter the map.'''
class Guard:
    def __init__(self, location, direction):
        # create local copies of the location and directions
        self.location = location.copy()
        self.direction = direction.copy()

    ''' make a deep copy of this guard and return a new guard '''
    def copy(self):
        return Guard(self.location, self.direction)

    ''' Turn in a clockwise direction '''
    def turn_clockwise(self):
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

    ''' Turn to find the first unobstructed path then move one step forward.'''
    def take_one_step(self, input_map):
        temp = self.location + self.direction
        # we are at an obstacle so turn
        if input_map[temp[0], temp[1]] == "#":
            self.turn_clockwise()
        #otherwise take a step
        else:
            self.location = temp

    '''Move in a straight line until the first occlusion is hit then turn.
       Return the locations on the map the guard has traversed.'''
    def move_to_next_turn(self, input_map):
        if self.direction == MapPuzzle.LEFT or self.direction == MapPuzzle.RIGHT:
            occ_ind = scan_line(input_map[self.location[0], self.location[1]::self.direction[1]], '#')
            cols = numpy.arange(self.location[1], self.location[1]+self.direction[1]*occ_ind, sign(self.direction[1]))
            rows = numpy.array([self.location[0]])
        else:
            occ_ind = scan_line(input_map[self.location[0]::self.direction[0], self.location[1]],'#')
            rows = numpy.arange(self.location[0], self.location[0]+self.direction[0]*occ_ind, sign(self.direction[0]))
            cols = numpy.array([self.location[1]])

        # if rows or cols are 0 this means we have not been able to move at all!
        # in this case do not move forward just turn the guard and return
        if rows.size > 0 and cols.size > 0:
            self.location = numpy.array([rows[-1], cols[-1]])

        self.turn_clockwise()
        return rows, cols

class PuzzleDay6(MapPuzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.guard = None
        self.map_size = numpy.array([0,0])

    def read_file(self):
        self.input = numpy.array(read_file_as_char_map(self.filename))

    # find the location and the direction the guard is facing
    # and put into our guard
    def find_guard(self):
        pos = self.find_start(self.input, '^')
        if pos is not None:  # facing up
            self.guard = Guard(pos, self.UP)
            return
        pos = self.find_start(self.input, 'v')
        if pos is not None:  # facing up
            self.guard = Guard(pos, self.DOWN)
            return
        pos = self.find_start(self.input, '<')
        if pos is not None:  # facing up
            self.guard = Guard(pos, self.LEFT)
            return
        pos = self.find_start(self.input, '>')
        if pos is not None:  # facing up
            self.guard = Guard(pos, self.RIGHT)

    # input_map is a 2D numpy array where # indicate obstacles
    def fill_in_next_line(self, input_map):
        rows, cols = self.guard.move_to_next_turn(self.input)
        input_map[rows, cols] = 'X'

    def part1(self):
        # first find where the guard is
        self.find_guard()

        # copy the map so the original input is preserved
        input_map = self.input.copy()

        # while the guard is not on the map boundary -- note for the upper bound we must add +1 to detect
        while numpy.all(self.guard.location > 0) and numpy.all(numpy.add(self.guard.location, 1) < self.input.shape):
            # fill in the next line
            self.fill_in_next_line(input_map)

        # count X in the map
        return numpy.count_nonzero(input_map == 'X')

    def part2(self):
        # first find where the guard is
        self.find_guard()

        #copy our map to create fake obstacles on
        temp_map = self.input.copy()

        # initialised counter
        count = 0

        # while the guard is not on the map boundary
        while not numpy.any(self.guard.location == 0) and not numpy.any(self.guard.location + 1 < self.input.shape):
            next_loc = self.guard.location + self.guard.direction

            # if our next position is not already an obstacle or a place we have previously traversed
            if temp_map[next_loc[0], next_loc[1]] not in ('#','X'):
                # try to place an obstacle in the next_loc and check if the guard enters a loop
                temp_map[next_loc[0], next_loc[1]] = '#'

                # create a temporary guard and turn it as there is now an occlusion in the way
                temp_guard = self.guard.copy()
                temp_guard.turn_clockwise()
                if is_in_loop(temp_map, temp_guard):
                    count += 1

                # remove the temporary obstacle from the map
                temp_map[next_loc[0], next_loc[1]] = '.'

            # place an X on the map where the guard currently is so we do not try to place an obstacle there
            temp_map[self.guard.location[0], self.guard.location[1]] = 'X'
            self.guard.take_one_step(temp_map)

        return count