import sys
import os
import time
import random
import string
from iasc_common import *

file_size_in_kb = int(sys.argv[1])

def get_time_str():
    timestr = time.strftime("%Y-%m-%dT%H:%M:%S")
    return timestr

def get_num_of_csv_lines(size):
    bytes_in_line = 18
    return size * 2 ** 10 / bytes_in_line 

def get_rand_csv_data():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(8))

num_of_lines = get_num_of_csv_lines(file_size_in_kb)
time_str = get_time_str()
filename = "temperature_humidity_records_" + time_str + ".000000.csv"
filepath = pending_dir + "/" + filename
print("generating " + filename + "...")

res = open(filepath, 'w')
res.write("time[sec], I[mA]")
for i in range(num_of_lines):
    line = get_rand_csv_data() + "," + get_rand_csv_data() + "\n"
    res.write(line)
res.close()

print("generated " + filepath)
