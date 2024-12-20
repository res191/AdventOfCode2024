from collections import deque
import numpy

from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

def compute_checksum(elem_number, start_ind, end_ind):
    return sum(elem_number * numpy.array(range(start_ind, end_ind)))

def compute_checksum2(input_array):
    start_ind = 0
    checksum = 0
    for i in range(0, len(input_array)):
        checksum += sum(input_array[i,0] * numpy.array(range(int(start_ind), int(start_ind+ input_array[i,1]))))
        start_ind += input_array[i,1]
    return checksum

class PuzzleDay9(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        self.input = ReadFiles.read_file_as_string(self.filename)

    def part1(self):
        # convert to a deque for ease of use
        input_deque = deque([int(elem) for elem in self.input])

        checksum_total = 0
        checksum_index = 0

        deque_start_counter = 0
        deque_end_counter = len(input_deque) // 2

        while input_deque:
            # for the first element in the list we need to add it to our checksum appropriately
            vals_to_fill = checksum_index + input_deque.popleft()
            dummy = compute_checksum(deque_start_counter, checksum_index, vals_to_fill)
            checksum_total += dummy

            # increment which starting element we are at
            deque_start_counter+=1
            # move the index counter
            checksum_index = vals_to_fill

            # we have reached the end of the list early so break this loop
            if not input_deque:
                break

            # the next element is a zero element so we fill it from the back of the deque
            zeros_to_fill = input_deque.popleft()
            while zeros_to_fill > 0:
                #if we have fewer zeros to fill than next elements we take what we can and leave the rest
                if zeros_to_fill < input_deque[-1]:
                    # take what we can
                    vals_to_fill = checksum_index + zeros_to_fill
                    dummy = compute_checksum(deque_end_counter, checksum_index, vals_to_fill)
                    checksum_total += dummy
                    checksum_index = vals_to_fill

                    # leave the rest
                    input_deque[-1] -= zeros_to_fill
                    # we are done with that element
                    zeros_to_fill = 0

                # otherwise fill the zeros as much as we can with the next element
                else:
                    # get how many of the zeros we can fill with our current end counter
                    vals_to_fill = checksum_index + input_deque[-1]
                    dummy = compute_checksum(deque_end_counter, checksum_index, vals_to_fill)
                    checksum_total += dummy
                    checksum_index = vals_to_fill

                    #deincrement our counters
                    deque_end_counter -= 1
                    # compute how many current zeros I still have to fill
                    zeros_to_fill -= input_deque.pop()
                    # remove the zero elements at the back of the deque
                    input_deque.pop()
        return checksum_total

    def part2(self):
        # convert the input to an array
        input_array = numpy.array([int(elem) for elem in self.input])

        # get the array we are going to fill
        sorted_array = numpy.zeros([len(self.input), 2])

        # insert the length of the zeros in the correct positions
        for x in range(1,len(input_array), 2):
            sorted_array[x,:] = [0, input_array[x]]

        for x in range(0,len(input_array), 2):
            sorted_array[x,:] = [x//2, input_array[x]]

        # the maximum free spaces still remaining
        # from the back of the array -- we go until before 0 since the first element can never be moved
        for i in range(len(input_array)-1, 0, -2):
            # I am searching for something of this size
            elem_size = input_array[i]

            # use the element id to find the index in my sorted array
            index = numpy.argmax(sorted_array[:,0] == i // 2)

            #find the first empty place the element can fit
            for j in numpy.where(sorted_array[0:index, 0] == 0)[0]:
                # the first block are the 0 indices so skip it
                if j == 0:
                    continue

                # if we fit
                if elem_size <= sorted_array[j , 1]:
                    # keep track of if we will have leftovers before changing the list
                    leftover_zeros = sorted_array[j, 1] - elem_size

                    # swap the file ids
                    sorted_array[j] = [sorted_array[index,0], elem_size]
                    sorted_array[index, 0] = 0

                    # if we have some remaining insert it
                    if leftover_zeros > 0:
                        sorted_array = numpy.insert(sorted_array, j + 1, [0,leftover_zeros], axis=0)

                    #remove the fileid from our list yet to be inserted
                    break

        # fill in what remains
        return compute_checksum2(sorted_array)