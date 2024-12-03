import sys
import time

from Modules import ProcessSafetyReports
from Modules import ReadFiles

def main (argv):
    start1 = time.time()
    input_list = ReadFiles.read_lines_special_parse(argv[0])
    print('Solution to puzzle 1 is: ', ProcessSafetyReports.compute_value(input_list))
    end1 = time.time()
    print('Taking ', end1-start1)

    start2 = time.time()
    input_list = ReadFiles.read_lines_special_parse_excludes(argv[0])
    print('Solution to puzzle 2 is: ', ProcessSafetyReports.compute_value(input_list))
    end2 = time.time()
    print('Taking ', end2-start2)

if __name__ == '__main__':
    main(sys.argv[1:])