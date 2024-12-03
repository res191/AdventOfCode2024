import sys
import time

from Modules import ReadFiles


def compute_value(number_pairs):
	return sum(int(row[0]) * int(row[1]) for row in number_pairs)

def main (argv):
    start1 = time.time()
    input_list = ReadFiles.read_lines_special_parse(argv[0])
    print('Solution to puzzle 1 is: ', compute_value(input_list))
    end1 = time.time()
    print('Taking ', end1-start1)

    start2 = time.time()
    input_list = ReadFiles.read_lines_special_parse_excludes(argv[0])
    print('Solution to puzzle 2 is: ', compute_value(input_list))
    end2 = time.time()
    print('Taking ', end2-start2)

if __name__ == '__main__':
    main(sys.argv[1:])