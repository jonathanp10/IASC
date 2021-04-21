import os, sys, inspect, logging, argparse

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from en.en_rx_manager import run_rx

if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_en.log"
    logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
    
    # initializations
    ignored_files = [] # TODO: check if we need this here
    en_id = os.environ.get('EN_ID')
    compression_mode = True
    
    # run rx manager - actually this runs the whole EN
    run_rx(compression_mode)