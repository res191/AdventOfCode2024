import numpy

from Modules.GenericPuzzle import Puzzle


def find_possible_trails(input_map, row_start, col_start, step_count, potential_trailends):
    # if we have no more trailheads to try and visit
    if len(potential_trailends) == 0:
        return potential_trailends

    if step_count == 9:
        if input_map[row_start, col_start] == 9:
            encode_position = row_start + (input_map.shape[0] * col_start)
            # we have reached the end so remove the item (if it exist in the list) and return
            return potential_trailends[potential_trailends != encode_position]
        else:
            return potential_trailends

    # populate my indices to check
    possible_rows = numpy.array([row_start - 1, row_start + 1, row_start, row_start])
    possible_cols = numpy.array([col_start, col_start, col_start - 1, col_start + 1])

    #  find the valid indices that have the correct next step
    valid_inds = [(x, y) for x, y in zip(possible_rows, possible_cols) if
                          0 <= x < input_map.shape[0] and 0 <= y < input_map.shape[1] and input_map[x, y] == step_count + 1]

    # we have another step to check and we still have trailends that we have not reached
    while len(valid_inds) != 0 and len(potential_trailends) !=0:
        next_step = valid_inds.pop()
        potential_trailends = find_possible_trails(input_map, next_step[0], next_step[1], step_count + 1, potential_trailends)

    return potential_trailends

class PuzzleDay10(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    # read file where ever character is an integer in its own element
    # cast everything to numpy arrays
    def read_file(self):
        f = open(self.filename, "r")
        self.input = numpy.array([list(map(int, list(line.rstrip()))) for line in f.readlines()])
        f.close()

    def part1(self):
        count = 0
        # for each 0 starting element
        trailheads = numpy.where(self.input == 0)
        potential_trailends = numpy.where(self.input == 9)
        potential_trailends = potential_trailends[0] + self.input.shape[0]*potential_trailends[1]

        # search to see if it reaches all of the 9
        for row_start, col_start in zip(trailheads[0], trailheads[1]):
            remaining_trails = find_possible_trails(self.input, row_start, col_start, 0, potential_trailends)
            count += len(potential_trailends) - len(remaining_trails)

        return count

    def part2(self):
        # first get my starting map filled with zeros
        seed_map = numpy.zeros(self.input.shape)

        # initialise the list to have 1 where the nines are
        seed_map[self.input == 9] = 1

        count = 0
        # get the indices of my rows and columns
        for current_number in range(9, 0, -1):
            inds_to_update = numpy.where(self.input == current_number - 1)
            for row, col in zip(inds_to_update[0], inds_to_update[1]):
                # populate my indices to check
                possible_rows = numpy.array([row - 1, row + 1, row, row])
                possible_cols = numpy.array([col, col, col - 1, col + 1])

                # need to be in bounds and match the correct number
                valid_inds = numpy.array([(x, y) for x, y in zip(possible_rows, possible_cols) if
                                          0 <= x < self.input.shape[0] and 0 <= y < self.input.shape[1] and self.input[
                                              x, y] == current_number])

                if valid_inds.size != 0:
                    # place the count into the current element
                    elem = sum(seed_map[valid_inds[:, 0], valid_inds[:, 1]])
                    seed_map[row, col] = elem
                    if (current_number - 1) == 0:
                        count += elem

        return count