import numpy

# return true if you get to the end of the file and have not swapped anything
def swap_incorrect_match(input_line, rulebook):
    for i in range(len(input_line)-1, 0, -1):
        rules_to_check = rulebook[rulebook[:,0]==input_line[i],1]
        for j in range(0, i):
            if numpy.any(rules_to_check==input_line[j]):
                # swap the two elements
                input_line[i], input_line[j] = input_line[j], input_line[i]
                return False
    return True

def validate_line(input_line, rulebook):
    for i in range(len(input_line)-1, 0, -1):
        rules_to_check = rulebook[rulebook[:,0]==input_line[i],1]
        for rule in rules_to_check:
            if numpy.any(input_line[0:i]==rule):
                return False
    return True

def generate_puzzle_one(input_list, rulebook):
    count = 0
    for input in input_list:
        if (validate_line(numpy.array(input), rulebook)):
            count += input[(len(input) - 1) // 2]
    return count

def generate_puzzle_two(input_list, rulebook):
    count = 0
    for input in input_list:
        input_arr = numpy.array(input)
        swaps = not swap_incorrect_match(input_arr, rulebook)

        while (not swap_incorrect_match(input_arr, rulebook)):
            pass

        if swaps:
            count += input_arr[(len(input) - 1) // 2]
    return count
