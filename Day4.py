import sys
import time

import numpy
from Modules import ProcessCrossword

def read_file(txtfile):
  f = open(txtfile, "r")
  input_list = []
  for line in f.readlines():
    input_list.append(numpy.array(list(line[0:-1])))
  return numpy.array(input_list)

def main (argv):
    input_array = read_file(argv[0])

    start1 = time.time()
    print('Solution to puzzle 1 is: ', ProcessCrossword.ProcessPuzzle(input_array))
    end1 = time.time()
    print('Taking ', end1-start1)

    start2 = time.time()
    print('Solution to puzzle 2 is: ', ProcessCrossword.ProcessPuzzlePerPatch(input_array))
    end2 = time.time()
    print('Taking ', end2-start2)

if __name__ == '__main__':
    main(sys.argv[1:])