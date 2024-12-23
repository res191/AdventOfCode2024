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
        count = 0
        # find where the path starts
        start = self.find_start(self.input, 'S')
        timed_map = self.fill_map(start)

        path = numpy.argwhere(self.input != '#')
        for step in path:
            count += self.find_shortcuts(timed_map, 2, step)
        return count

    def find_shortcuts(self, timed_map, cheat_length, start_pos):
        # for the row
        count = 0
        start_int = int(timed_map[start_pos[0], start_pos[1]])

        for i in range (start_pos[0] - cheat_length, start_pos[0] + cheat_length + 1):
            # for the column
            for j in range(start_pos[1] - cheat_length, start_pos[1] + cheat_length + 1):
                row_step = abs(start_pos[0] - i)
                col_step = abs(start_pos[1] - j)

                # this is not a valid  just continue
                if (row_step + col_step > cheat_length or not self.position_in_bounds(self.input,numpy.array([i, j]))
                        or self.input[i, j]=='#'):
                    continue

                # shortcut is the start and end position minus the number of steps
                shortcut = int(timed_map[i,j]) - start_int - row_step - col_step
                if shortcut > self.min_shortcut:
                    count += 1

        return count

    def part2(self):
        count = 0
        # find where the path starts
        start = self.find_start(self.input, 'S')
        timed_map = self.fill_map(start)

        path = numpy.argwhere(self.input != '#')
        for step in path:
            count += self.find_shortcuts(timed_map, 20, step)
        return count