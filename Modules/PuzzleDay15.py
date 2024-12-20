import numpy

from Modules.GenericPuzzle import MapPuzzle
from Modules import ReadFiles

class PuzzleDay15(MapPuzzle):
    def __init__(self, filename):
        super().__init__(filename)
        self.map = None
        self.robot = None

    def read_file(self):
        file_output = ReadFiles.read_file_as_list(self.filename)

        index = file_output.index('')
        self.map = numpy.array([list(line) for line in file_output[0:index]])
        self.input = "".join(file_output[index+1::])

    # update the map based on the robot and the step
    def take_step(self, step):
        # figure out how many boxes we will push
        new_pos = self.robot + step

        # cannot take a step so return
        if self.map[new_pos[0], new_pos[1]] == '#':
            return
        # can take a step but there is a box in the way
        elif self.map[new_pos[0], new_pos[1]] in ('O','[',']'):
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
        self.robot = self.robot + step
        self.map[self.robot[0],self .robot[1]] = '@'

    def run_steps(self):
        for elem in self.input:
            match elem:
                case "^":
                    self.take_step(self.UP)
                case "v":
                    self.take_step(self.DOWN)
                case ">":
                    self.take_step(self.RIGHT)
                case "<":
                    self.take_step(self.LEFT)
                case _:
                    print("Error unrecognised command!")

    def part1(self):
        # initialise the robot
        self.robot = self.find_start(self.map,'@')

        # run through the steps
        self.run_steps()

        # compute the count
        box_pos = numpy.argwhere(self.map=='O')
        count = sum([box[0] * 100 + box[1] for box in box_pos])
        return count

    def create_big_map(self):
        # repeat
        big_map = numpy.repeat(self.map,2, axis=1)

        # fix the special cases
        possible_robots = numpy.argwhere(big_map == '@')
        # replace the right most robot
        if sum(possible_robots[0] - possible_robots[1]) < 0:
            big_map[possible_robots[1,0],possible_robots[1,1]] ='.'
            self.robot = possible_robots[0]
        else:
            big_map[possible_robots[0,0],possible_robots[0,1]] ='.'
            self.robot = possible_robots[1]

        # boxes are more complicated
        boxes = numpy.argwhere(big_map == 'O')
        for elem in boxes:
            # if directly to the left we have anything that is not an old box or the left side of a box
            # place the right side of a box
            if big_map[elem[0], elem[1]-1] in ('.','#','@',']'):
                big_map[elem[0],elem[1]]='['
            # if directly to the right we have anything that is not an older box or the right side of a box
            # place the left side of a box
            elif big_map[elem[0], elem[1]+1] in ('.','#','@','['):
                big_map[elem[0],elem[1]]=']'
            elif big_map[elem[0], elem[1]-1] == '[':
                big_map[elem[0],elem[1]]=']'
            elif big_map[elem[0], elem[1]-1] == ']':
                big_map[elem[0],elem[1]]='['

        # just double check here we have no more old boxes
        if numpy.any(numpy.ndarray.flatten(big_map)=='O'):
            print("Old boxes still exist, fix your code!")

        return big_map

    def part2(self):
        #first we must expand the map
        big_map = self.create_big_map()