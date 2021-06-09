import os, sys, inspect, logging, lzma, threading, time
from queue import Queue as Queue



# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from common.iasc_common import *
from gw.gw_rx_manager import run_rx, handle_msgs
from common.iasc_dir_cleaner import dir_cleanup


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    LOG_FILE_NAME = "iasc_gw.log"
    if args.dbg:
        logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.DEBUG, format="%(asctime)s:%(levelname)-8s %(message)s")
    else: 
        logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")

    # initializations
    ignored_lst = []
    rx_fifo = Queue()

    compression_mode = args.comp
    if compression_mode:
       compression_mode_str = "Compression Mode is ON"
    else:
       compression_mode_str = "Compression Mode is OFF"
    logging.info("[{}]: Compression mode is {}".format(__name__, compression_mode_str))

    init_stats_csv("gw_stats.csv")

    # run gw rx fifo handler
    run_rx_fifo_handler = threading.Thread(target=handle_msgs, args = (rx_fifo, ignored_lst, compression_mode,))
    run_rx_fifo_handler.start()
    
    # run gw rx
    run_rx_t = threading.Thread(target=run_rx, args = (rx_fifo,args.sim))
    run_rx_t.start()


    while True:
      time.sleep(cleaner_sleep_time_in_sec)
      gw_cleanup_t = threading.Thread(target=dir_cleanup, args = (ignored_lst, gw_queues_dir,))
      #gw_cleanup_t.start()
