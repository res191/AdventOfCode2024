import numpy

from Modules.GenericPuzzle import  MapPuzzle
from Modules.ReadFiles import read_file_as_char_map

class PuzzleDay20(MapPuzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.min_shortcut = 100

    def read_file(self):
        self.input = numpy.array(read_file_as_char_map(self.filename), dtype='<U5')

    def fill_map(self, start):
        timed_map = self.input.copy()
        timed_map[start[0], start[1]] = str(0)

        #initialise the counter
        counter = 1

        # while we still have a starting position
        while len(start) != 0:
            # find the next direction with a '.'
            possible_step = [start + x for x in self.DIRECTIONS]
            for step in possible_step:
                # if we are at our next step increment the walker
                if timed_map[step[0], step[1]] =='.':
                    timed_map[step[0], step[1]] = str(counter)
                    counter += 1
                    start = step
                    continue
                # we are at the end so replace the start and end characters with numbers before returning
                elif timed_map[step[0], step[1]] == 'E':
                    timed_map[step[0], step[1]] = str(counter)
                    return timed_map

    def part1(self):
        # find where the path starts
        start = self.find_start(self.input,'S')
        timed_map = self.fill_map(start)

        # find all the possible places one could cheat
        blocks = numpy.argwhere(self.input == '#')

        # remove any blocks that are on the edges
        blocks = blocks[ numpy.all(blocks > 0, axis = 1) ]
        blocks = blocks[ numpy.all(blocks < numpy.array(self.input.shape)  -1, axis = 1) ]

        # for each potential cheat block
        count = 0
        for cheat in blocks:
            # because some walls might have no valid shortcut reinitialise the value to 0 every time
            shortcut = 0

            # if a new path would be created in the UP-DOWN direction
            if self.input[cheat[0]+1, cheat[1]] != '#' and self.input[cheat[0]-1, cheat[1]] != '#':
                shortcut = abs(int(timed_map[cheat[0]+1, cheat[1]]) - int(timed_map[cheat[0]-1, cheat[1]]))
            # if a new path would be created in the LEFT-RIGHT direction
            elif self.input[cheat[0], cheat[1]+1] != '#' and  self.input[cheat[0], cheat[1]-1] != '#':
                shortcut = abs(int(timed_map[cheat[0], cheat[1]+1]) - int(timed_map[cheat[0], cheat[1] - 1]))

            # note here we are subtracting 2 from the shortcut because the cheat takes 2 picoseconds
            if  shortcut - 2 > self.min_shortcut:
                count += 1

        return count

    def part2(self):
        pass