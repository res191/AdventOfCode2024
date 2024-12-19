
def read_file_as_int_list(txtfile):
  f = open(txtfile, "r")
  input_list = [list(map(int, line.split())) for line in f.readlines()]
  f.close()
  return input_list

def read_file_as_string(txtfile):
  return "".join(open(txtfile,"r").read().splitlines())

def read_file_as_list(txtfile):
  f = open(txtfile, "r")
  input_list = [line.rstrip() for line in f.readlines()]
  f.close()
  return input_list

''' Here a map is a 2D list where each item describes on position.'''
def read_file_as_char_map(txtfile):
  f = open(txtfile, "r")
  input_map = [list(line.rstrip()) for line in f.readlines()]
  f.close()
  return input_map
