import os, sys, inspect, logging

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from common.iasc_common import *
from gw.gw_rx_manager import run_rx


if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_gw.log"
    logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
    
    # initializations
    ignored_lst = []
    compression_mode = True
    
    # run gw rx
    run_rx(compression_mode)
