import numpy
from sklearn.utils.estimator_checks import check_get_feature_names_out_error

from Modules.GenericPuzzle import MapPuzzle
from Modules import ReadFiles


class PuzzleDay18(MapPuzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.map = None

    def create_map(self):
        self.map = numpy.full([71,71], numpy.nan)
        for i in range(0,1024):
            self.map[self.input[i,0], self.input[i,1]] = numpy.inf

    # here the input is the position of the bits overwritten in the map
    def read_file(self):
        file_output = ReadFiles.read_file_as_list(self.filename)
        self.input = numpy.array([list(map(int, list(line.split(',')))) for line in file_output])

    def evaluate_next_step(self, map, num_steps):
        inds_to_update = numpy.where(map == num_steps)

        # we have no more valid moves to update so return with an error code
        if len(inds_to_update[0]) == 0:
            return -1

        # for each of our current min steps
        for row, col in zip(inds_to_update[0], inds_to_update[1]):
            # get each of the neighbors
            for dir in self.DIRECTIONS:
                next_row = row + dir[0]
                next_col = col + dir[1]
                # we are not bounds skip
                if next_row < 0 or next_row > map.shape[0] - 1 or next_col < 0 or next_col > map.shape[1] - 1:
                    continue

                # we are at our goal so step and return
                if next_row == 70 and next_col == 70:
                    return num_steps + 1

                # we are not at our goal, check if we have a valid neighbor
                if numpy.isnan(map[next_row, next_col]):
                    map[next_row, next_col] = num_steps + 1
        # if we have made it this far we need to continue
        return self.evaluate_next_step(map, num_steps + 1)

    def part1(self):
        self.create_map()
        # initialise for the region growing
        self.map[0,0] = 0
        return self.evaluate_next_step(self.map, 0)

    def part2(self):
        self.create_map()
        self.map[0,0] = 0

        counter = 1023
        # this is only for sense checking as if part 1 passes this must too
        steps = self.evaluate_next_step(self.map.copy(), 0)
        # while we still have a valid path to the exit
        while steps != -1:
            # increment the counter
            counter +=1
            #get the next bit and place it on the map
            self.map[self.input[counter, 0], self.input[counter,1]] = numpy.inf
            steps = self.evaluate_next_step(self.map.copy(), 0)

        return self.input[counter]