import sys
import os

sensor_id = sys.argv[1]
file_size_in_kb = sys.argv[2]

def get_time_str():
    return "070394_0225"  # TODO 

def get_num_of_csv_lines(size):
    return 10  # TODO 

def get_rand_csv_data():
    return "ABC"

num_of_lines = get_num_of_csv_lines(file_size_in_kb)
time_str = get_time_str()
filename = sensor_id + "_" + time_str + ".csv"
print("generating " + filename + "...")

res = open(filename, 'w')
res.write("time[sec], I[mA]")
for i in range(num_of_lines):
    line = get_rand_csv_data() + "," + get_rand_csv_data() + "\n"
    res.write(line)
res.close()

print("generated.")