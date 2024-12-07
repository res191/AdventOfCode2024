import numpy
from numpy.ma.core import concatenate
from sympy.integrals.manualintegrate import substitution_rule

# check if num2 is fully contained at the end of num1
# if so return the remaining digits of num1 as a string
# otherwise return an emtry string
def strip_last_digits_of_num(num1, num2):
    str1 = str(num1)
    str2 = str(num2)

    if (str1[len(str1)-len(str2)::] == str2):
        return str1[:len(str1)-len(str2)]
    return ''

def check_rule(input_list):
    # if there are only two numbers:
    #  -return the equality (true if equal, false otherwise)
    if len(input_list) == 2:
        return input_list[0] == input_list[1]

    # if the last element of the input array is more than the first element
    # return false
    if input_list[0] < input_list[-1]:
        return False

    # if the first number is divisible by the last
    if input_list[0] % input_list[-1] == 0:
        # create a new list to test
        multiplication_rule = [input_list[0]//input_list[-1]] + input_list[1:-1]
        if check_rule((multiplication_rule)):
            return True

    #otherwise check with a minus
    subtraction_rule = [input_list[0] - input_list[-1]] + input_list[1:-1]
    return check_rule(subtraction_rule)

def check_new_rule(input_list):
    # if there are only two numbers:
    #  -return the equality (true if equal, false otherwise)
    if len(input_list) == 2:
        return input_list[0] == input_list[1]

    # if the last element of the input array is more than the first element
    # return false
    if input_list[0] < input_list[-1]:
        return False

    # if the first number is divisible by the last
    if input_list[0] % input_list[-1] == 0:
        # create a new list to test
        multiplication_rule = [input_list[0]//input_list[-1]] + input_list[1:-1]
        if check_new_rule(multiplication_rule):
            return True

    #otherwise check with a minus
    subtraction_rule = [input_list[0] - input_list[-1]] + input_list[1:-1]
    if check_new_rule(subtraction_rule):
        return True

    # otherwise check the concatentation can occur
    new_num = strip_last_digits_of_num(input_list[0], input_list[-1])
    if not new_num:
        return False

    concatenate_rule = [int(new_num)] + input_list[1:-1]
    return check_new_rule(concatenate_rule)

def compute_sum_mult(input_list):
    sum = 0
    for input_line in input_list:
        if (check_rule((input_line))):
            sum+=input_line[0]
    return sum

def compute_sum_mult_cat(input_list):
    sum = 0
    for input_line in input_list:
        if (check_rule((input_line))):
            sum+=input_line[0]
        elif (check_new_rule(input_line)):
            sum+=input_line[0]
    return sum