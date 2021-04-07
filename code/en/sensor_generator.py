import os, sys, inspect
import time
from datetime import datetime
import random
import string

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from common.iasc_common import *

file_size_in_kb = int(sys.argv[1])




def get_time_str():
    timestr = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")
    return timestr

def get_num_of_csv_lines(size):
    bytes_in_line = 18
    return size * 2 ** 10 / bytes_in_line 

def get_rand_csv_data():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(8))


num_of_lines = get_num_of_csv_lines(file_size_in_kb)
time_str = get_time_str()
filename = "rpi_lora_lte_records_" + time_str + ".csv"
filepath = pending_dir + "/" + filename
print("generating " + filename + "...")

if not os.path.exists(pending_dir):
    os.mkdir(pending_dir)
res = open(filepath, 'w')
res.write("time[sec], I[mA]")
for i in range(num_of_lines):
    line = get_rand_csv_data() + "," + get_rand_csv_data() + "\n"
    res.write(line)
res.close()

print("generated " + filepath)
