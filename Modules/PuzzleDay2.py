import numpy

from Modules.GenericPuzzle import Puzzle
from Modules import ReadFiles

def get_first_bad_element(report):
    is_asc = numpy.sign(report[0] - next(i for i in report if i != report[0]))

    for i in range(1, len(report)):
        diff = report[i - 1] - report[i]
        if (numpy.sign(diff) != is_asc) or abs(diff) > 3:
            return i

    return numpy.nan

def is_report_safe(report):
    # is the report going up or down?
    is_asc = numpy.sign(report[0] - report[-1])
    if is_asc == 0:  # indicates first and last element are a duplicate so return
        return False

    # for each element in the list that is not the first
    for i in range(1, len(report)):
        # calculate the difference
        diff = report[i - 1] - report[i]
        # if we are not going the corrct direction or the step is too big
        if numpy.sign(diff) != is_asc or abs(diff) > 3:
            return False
    # if we reach here we have correctly read the report
    return True

def process_safety_reports(report_list, damper=False):
    count = 0
    for report in report_list:
        if is_report_safe(report):
            count += 1
        elif damper:
            bad_ind = get_first_bad_element(report)

            if is_report_safe(report[0:bad_ind - 1] + report[bad_ind:]):
                count += 1
            elif is_report_safe(report[0:bad_ind] + report[bad_ind + 1:]):
                count += 1

    return count

class PuzzleDay2(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    """ Each report is a list of integers.
    """
    def read_file(self):
        self.input = ReadFiles.read_file_as_int_list(self.filename)

    """ Process the inputs without adding the damping term
    """
    def part1(self):
        return process_safety_reports(self.input)

    """ Process the inputs adding the damping term
    """
    def part2(self):
        return process_safety_reports(self.input, True)

