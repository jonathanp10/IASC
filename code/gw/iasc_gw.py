import os, sys, inspect, logging, lzma, argparse, threading, time



# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from common.iasc_common import *
from gw.gw_rx_manager import run_rx
from common.iasc_dir_cleaner import dir_cleanup


if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_gw.log"
    logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
    
    # initializations
    ignored_lst = []
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-comp', required=False, action = "store_true", help = "in this mode en compress all tx files")
    arg_parser.add_argument('-compression', required=False, action = "store_true", help = "in this mode en compress all tx files")
    args = arg_parser.parse_args()

    compression_mode = (args.comp or args.compression)
    if compression_mode:
       compression_mode_str = "Compression Mode is ON"
    else:
       compression_mode_str = "Compression Mode is OFF"
    logging.info("[{}]: Compression mode is {}".format(__name__, compression_mode_str))

    init_stats_csv("gw_stats.csv")

    # run gw rx
    run_rx_t = threading.Thread(target=run_rx, args = (ignored_lst, compression_mode,))
    run_rx_t.start()


    while True:
      time.sleep(60)
      en_cleanup_t = threading.Thread(target=dir_cleanup, args = (ignored_lst, gw_queues_dir,))
      en_cleanup_t.start()
