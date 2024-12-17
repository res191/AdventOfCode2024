
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
