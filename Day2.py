
import sys
import time

from Modules import ProcessSafetyReports
from Modules import ReadFiles

def main (argv):
    input_list = ReadFiles.read_lines_as_list((argv[0]))
    start1 = time.time()
    print('Solution to puzzle 1 is: ', ProcessSafetyReports.process_safety_reports(input_list))
    end1 = time.time()
    print('Taking ', end1-start1)

    start2 = time.time()
    print('Solution to puzzle 2 is: ', ProcessSafetyReports.process_safety_reports(input_list, True))
    end2 = time.time()
    print('Taking ', end2-start2)

if __name__ == '__main__':
    main(sys.argv[1:])