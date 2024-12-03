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

def read_lines_special_parse(txtfile):
  f = open(txtfile, "r")
  input_list = list()
  for line in f.readlines():
    input_list = input_list + re.findall('mul\(\d{1,3},\d{1,3}\)', line)
  return input_list
