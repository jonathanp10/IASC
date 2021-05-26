import os, sys, inspect, logging, argparse, threading, time
from timeit import default_timer as timer

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from common.iasc_dir_cleaner import dir_cleanup
from en.en_rx_manager import run_rx


if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_en.log"
    logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
    
    # initializations
    ignored_files = [] 
    
    
    arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument('en_id', action='store', nargs='*', type=int, help = "EN_ID", default=os.environ.get('EN_ID'))
    arg_parser.add_argument('-comp', required=False, action = "store_true", help = "in this mode en compress all tx files")
    arg_parser.add_argument('-compression', required=False, action = "store_true", help = "in this mode en compress all tx files")
    args = arg_parser.parse_args()

    compression_mode = (args.comp or args.compression)
    # global en_id
    # en_id = args.en_id
    if compression_mode:
       compression_mode_str = "Compression Mode is ON"
    else:
       compression_mode_str = "Compression Mode is OFF"
    logging.info("[{}]: Compression mode is {}".format(__name__, compression_mode_str))
        
    # run rx manager - actually this runs the whole EN
    init_stats_csv("en_stats.csv")

    run_rx_t = threading.Thread(target=run_rx, args = (ignored_files, compression_mode,))
    run_rx_t.start()
    
    while True:
      time.sleep(60)
      en_cleanup_t = threading.Thread(target=dir_cleanup, args = (ignored_files,pending_dir,))
      #en_cleanup_t.start()
    



