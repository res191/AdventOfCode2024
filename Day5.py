import sys
import time
import numpy

from Modules import ProcessPrinterQueue

def read_file(txtfile):
    f = open(txtfile, "r")
    all_lines = f.readlines()

    for index, line in enumerate(all_lines):
        if line == "\n":
            break

    rulebook = numpy.array([list(map(int, line.split('|'))) for line in all_lines[:index-1]])
    input_list = [list(map(int, line.split(','))) for line in all_lines[index+1:]]
    return rulebook, input_list


def main (argv):
    rulebook, input_array = read_file(argv[0])

    start1 = time.time()
    print('Solution to puzzle 1 is: ', ProcessPrinterQueue.generate_puzzle_one(input_array, rulebook))
    end1 = time.time()
    print('Taking ', end1 - start1)

    start2 = time.time()
    print('Solution to puzzle 2 is: ', ProcessPrinterQueue.generate_puzzle_two(input_array, rulebook))
    end2 = time.time()
    print('Taking ', end2 - start2)

if __name__ == '__main__':
    main(sys.argv[1:])