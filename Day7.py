import sys
import time
import numpy
import re

from Modules import BridgeOperators

def read_file(txtfile):
    f = open(txtfile, "r")
    input_list = [list(map(int, re.split(": | ", line))) for line in f.readlines()]
    return input_list

def main (argv):
    input_list = read_file(argv[0])

    start1 = time.time()
    print('Solution to puzzle 1 is: ', BridgeOperators.compute_sum_mult(input_list))
    end1 = time.time()
    print('Taking ', end1 - start1)

    start2 = time.time()
    print('Solution to puzzle 2 is: ',  BridgeOperators.compute_sum_mult_cat(input_list))
    end2 = time.time()
    print('Taking ', end2 - start2)

if __name__ == '__main__':
    main(sys.argv[1:])