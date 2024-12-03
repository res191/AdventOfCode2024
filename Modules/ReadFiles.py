import numpy
import re

# Read in a text file and return as an 2D-array
def read_lines_as_numpy(txtfile):
  f = open(txtfile, "r")
  input_list =[list(map(int, line.split())) for line in f.readlines()]
  input_np = numpy.array(input_list)
  return input_np

def read_lines_as_list(txtfile):
  f = open(txtfile, "r")
  input_list =[list(map(int, line.split())) for line in f.readlines()]
  return input_list

def special_parse_line(line):
  numbers = list()
  all_items = re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)
  for item in all_items:
    pair = re.findall(r'\d{1,3}', item)
    if (len(pair) != 2):
      print('Error processing', item)
    else:
      numbers.append(pair)
  return numbers

def read_lines_special_parse(txtfile):
  f = open(txtfile, "r")
  lines = "".join([line.strip('\n')  for line in f.readlines()])
  return  special_parse_line(lines)

def read_lines_special_parse_excludes(txtfile):
  f = open(txtfile, "r")
  lines = "".join([line.strip('\n')  for line in f.readlines()])
  all_list = re.split('do\(\)', lines)

  input_list = list()
  for item in all_list:
    good_item = re.split('don\'t\(\)', item, maxsplit=1)
    input_list = input_list + special_parse_line(good_item[0])

  return input_list