import numpy
import re

from sympy import false

def ProcessPuzzlePerPatch(input_array):
    number_items = 0
    # first find all the A not on the edges of the array
    a_inds = numpy.swapaxes(numpy.where(input_array[1:-1,1:-1]=='A'),0,1)
    for item in a_inds:
        if ScanPatch(input_array[item[0]:item[0]+3, item[1]:item[1]+3]):
            number_items+=1
    return number_items

def ProcessPuzzle(input_array):
    number_items = 0

    # Slice the first direction
    for row in range(0, input_array.shape[0]):
        number_items+=ScanLine("".join(input_array[row,:]))
    #Slice the second direction
    for col in range(0, input_array.shape[1]):
        number_items+=ScanLine("".join(input_array[:,col]))

    # minus 4 because we need at least 4 elements to make XMAS
    max_offset = max(input_array.shape) - 3
    #Slice in the diagonal
    for step in range(-max_offset, max_offset):
        number_items+=ScanLine("".join(numpy.diagonal(input_array, offset=step)))

    #Slice in the off diagonal
    flip_array = numpy.fliplr(input_array)
    for step in range(-max_offset, max_offset):
        number_items+=ScanLine("".join(numpy.diagonal(flip_array, offset=step)))

    return number_items

def ScanLine(input_line):
    forward_items = re.findall(r'XMAS', input_line)
    backward_items = re.findall(r'SAMX', input_line)
    return len(forward_items) + len(backward_items)

# Expects as input a 3x3 array
def ScanPatch(sub_array):
    # there are four options
    if not(sub_array[0,0] =='S' and sub_array[2,2]=='M') and not(sub_array[0,0] =='M' and sub_array[2,2]=='S'):
        return False
    elif not(sub_array[0,2] =='S' and sub_array[2,0]=='M') and not(sub_array[0,2] =='M' and sub_array[2,0]=='S'):
        return False
    return True