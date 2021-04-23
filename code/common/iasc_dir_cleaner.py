import os, time, logging, inspect, sys, psutil

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from common.iasc_common import *

def dir_cleanup(ignored_list, dir_2_clean):
   logging.info("[{}]: Cleaner in progress!\n".format(__name__))

   age_threshold = 60 * 1
   aggressive_mode_switch = "OFF"
   disk_usage = psutil.disk_usage('/')  # returns (total,used,free)
   if disk_usage[1]/disk_usage[0] >= 0.95: # deletes all files in ignored_list
      age_threshold = 0
      aggressive_mode_switch = "ON"
   logging.info("[{}]: Cleaner aggressive mode is {}\n".format(__name__,  aggressive_mode_switch))

   now = time.time()
   deleted_counter = 0
   for f in os.listdir(dir_2_clean):
      age = now - os.stat(os.path.join(dir_2_clean,f)).st_mtime
      if age > age_threshold and (f in ignored_list):
         logging.info("[{}]: Cleaner removed file with age {}: {}\n".format(__name__,  age, f))
         os.remove(os.path.join(dir_2_clean, f))
         ignored_list.remove(f)
         deleted_counter += 1
   logging.info("[{}]: Cleaner is done: {} files were deleted\n".format(__name__, deleted_counter))

