import re

from Modules.GenericPuzzle import Puzzle

# check if num2 is fully contained at the end of num1
# if so return the remaining digits of num1 as a string
# otherwise return an empty string
def strip_last_digits_of_num(num1, num2):
    str1 = str(num1)
    str2 = str(num2)

    if str1[len(str1)-len(str2)::] == str2:
        return str1[:len(str1)-len(str2)]
    return ''

def check_rule(input_list, use_concate):
    # if there are only two numbers:
    #  -return the equality (true if equal, false otherwise)
    if len(input_list) == 2:
        return input_list[0] == input_list[1]

    # if the last element of the input array is more than the first element
    # return false
    if input_list[0] < input_list[-1]:
        return False

    # if the first number is divisible by the last check the multiplication rule
    if (input_list[0] % input_list[-1] == 0 and
            check_rule([input_list[0]//input_list[-1]] + input_list[1:-1], use_concate)):
        return True

    #otherwise check with a subtraction
    if check_rule([input_list[0] - input_list[-1]] + input_list[1:-1], use_concate):
        return True

    # if we want to exclude concatenation and we have reached here return false
    if not use_concate:
        return False

    # check if we can concatenate
    new_num = strip_last_digits_of_num(input_list[0], input_list[-1])
    if not new_num:
        return False

    # if we can concatenate continue the recursion
    return check_rule([int(new_num)] + input_list[1:-1], use_concate)

class PuzzleDay7(Puzzle):
    def __init__(self, filename):
        super().__init__(filename)

    def read_file(self):
        f = open(self.filename, "r")
        self.input = [list(map(int, re.split(": | ", line))) for line in f.readlines()]
        f.close()

    # note to self try to clean up with a filter
    def part1(self):
        val = 0
        for input_line in self.input:
            if check_rule(input_line, False):
                val += input_line[0]
        return val

    def part2(self):
        val = 0
        for input_line in self.input:
            if check_rule(input_line, False):
                val += input_line[0]
            elif check_rule(input_line, True):
                val += input_line[0]
        return val