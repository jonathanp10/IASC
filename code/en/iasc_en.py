import os, sys, inspect, logging, threading, time #,argparse
from timeit import default_timer as timer

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from common.iasc_dir_cleaner import dir_cleanup
from en.en_rx_manager import run_rx


if __name__ == "__main__":
    # initializations
    ignored_files = [] 
    args = parse_args(sys.argv[1:])
    
    LOG_FILE_NAME = "iasc_en.log"
    if args.dbg:
        logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.DEBUG, format="%(asctime)s:%(levelname)-8s %(message)s")
    else:
        logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")

    compression_mode = args.comp
    if compression_mode:
       compression_mode_str = "Compression Mode is ON"
    else:
       compression_mode_str = "Compression Mode is OFF"
    logging.info("[{}]: Compression mode is {}".format(__name__, compression_mode_str))
        
    # run rx manager - actually this runs the whole EN
    init_stats_csv("en_stats.csv")

    run_rx_t = threading.Thread(target=run_rx, args = (ignored_files, compression_mode, args.sim))
    run_rx_t.start()
    
    while True:
      time.sleep(cleaner_sleep_time_in_sec)
      en_cleanup_t = threading.Thread(target=dir_cleanup, args = (ignored_files,pending_dir,))
      #en_cleanup_t.start()
    



