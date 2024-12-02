
import sys
from Modules import ProcessSafetyReports
from Modules import ReadFiles

def main (argv):
    input_list = ReadFiles.read_lines_as_list((argv[0]))
    print('Solution to puzzle 1 is: ', ProcessSafetyReports.process_safety_reports(input_list))

if __name__ == '__main__':
    main(sys.argv[1:])