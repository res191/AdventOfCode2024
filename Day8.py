import sys

import time
import numpy

from Modules import FindAntinodes

def read_file(txtfile):
    f = open(txtfile, "r")
    input_map=[]
    for line in f.readlines():
        input_map.append(list(line.rstrip()))
    return input_map

def main(argv):
    input_map = numpy.array(read_file(argv[0]))

    start1 = time.time()
    print('Solution to puzzle 1 is: ', FindAntinodes.place_antinodes(input_map.copy()))
    end1 = time.time()
    print('Taking ', end1 - start1)

    start2 = time.time()
    print('Solution to puzzle 2 is: ',FindAntinodes.place_harmonic_antinodes(input_map.copy()))
    end2 = time.time()
    print('Taking ', end2 - start2)

if __name__ == '__main__':
    main(sys.argv[1:])