import numpy

from Modules.GenericPuzzle import sign
from Modules.GenericPuzzle import MapPuzzle
from Modules import ReadFiles

def move_boxes(input_map, boxes, step):
    # first get my box characters
    box_sym = input_map[boxes[:,0], boxes[:,1]]

    # reset the current boxes
    input_map[boxes[:,0], boxes[:,1]] = '.'

    # move the boxes to the new locations
    new_boxes = boxes + step
    input_map[new_boxes[:,0], new_boxes[:,1]] = box_sym

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

    ''' Find the location of the boxes which will be moved. '''
    def get_moving_boxes(self, input_map, step):
        boxes= numpy.array([[],[]], dtype='int64').T

        # compute the bounds of the region corresponding to the boxes
        box_pos = self.robot + step

        # robot moving right or left can only have one row
        if step[0] == 0:
            # figure out the position after our boxes end
            while input_map[box_pos [0], box_pos[1]] in ('O','[',']'):
                boxes = numpy.append(boxes, [box_pos], axis=0)
                box_pos = box_pos + step

            #the region we are trying to move
            return boxes

        # for the current row
        row_to_scan = numpy.array([box_pos])
        # we have some portion that might have a box
        while len(row_to_scan) != 0:
            curr_row = numpy.array([[],[]], dtype='int64').T
            # for each possible box in the current row
            for elem in row_to_scan:
                # if we are at the left end of a box add
                if input_map[elem[0],elem[1]] =='[':
                    curr_row = numpy.append(curr_row, [elem], axis=0)
                    curr_row = numpy.append(curr_row, [elem + self.RIGHT], axis=0)
                # if we are at the right end of a box
                elif input_map[elem[0], elem[1]] == ']':
                    curr_row = numpy.append(curr_row, [elem], axis=0)
                    curr_row = numpy.append(curr_row, [elem + self.LEFT], axis=0)
                # we have a small box
                elif input_map[elem[0], elem[1]] == 'O':
                    curr_row = numpy.append(curr_row, [elem], axis=0)
            # make sure we only add each box once
            curr_row = numpy.unique(curr_row, axis=0)
            # put in our boxes to move
            boxes = numpy.append(boxes, curr_row, axis=0)
            # get the next row we are going to scan
            row_to_scan = curr_row + step

        return boxes

    # update the map based on the robot and the step
    def take_step(self, input_map, step):
        # get the new robot pos
        new_pos = self.robot + step

        # cannot take a step so return
        if input_map[new_pos[0], new_pos[1]] == '#':
            return

        # there is a box in the way of our step
        elif input_map[new_pos[0], new_pos[1]] in ('O','[',']'):
            # get the region we are going to be moving
            boxes = self.get_moving_boxes(input_map, step)

            # if we have a box-wall overlap we cannot move so return
            new_boxes = boxes + step
            if  numpy.any(input_map[new_boxes[:,0], new_boxes[:,1]] == '#'):
              return

            # update our map
            move_boxes(input_map, boxes, step)

        # move our robot and update the map
        input_map[self.robot[0],self.robot[1]] = '.'
        self.robot = self.robot + step
        input_map[self.robot[0],self .robot[1]] = '@'

    '''Convert the input into the series of steps to take.'''
    def run_steps(self, input_map):
        for elem in self.input:
            match elem:
                case "^":
                    self.take_step(input_map, self.UP)
                case "v":
                    self.take_step(input_map, self.DOWN)
                case ">":
                    self.take_step(input_map, self.RIGHT)
                case "<":
                    self.take_step(input_map, self.LEFT)
                case _:
                    print("Error unrecognised command!")

    def part1(self):
        # initialise the robot
        self.robot = self.find_start(self.map,'@')

        # run through the steps
        input_map = self.map.copy()
        self.run_steps(input_map)

        # compute the count
        box_pos = numpy.argwhere(input_map=='O')
        count = sum([box[0] * 100 + box[1] for box in box_pos])
        return count

    ''' Expand the map by two!
        This will also re-initialise the robot position, as the location must be found to ensure it is not duplicated.'''
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
        #first we must expand the map, this will also initialise the robot!
        big_map = self.create_big_map()
        self.run_steps(big_map)

        # count is now more or less the same, use the left edge
        box_pos = numpy.argwhere(big_map=='[')
        count = sum([box[0] * 100 + box[1] for box in box_pos])
        return count