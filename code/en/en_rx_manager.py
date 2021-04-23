import os, sys, inspect, logging, argparse
from timeit import default_timer as timer

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from en.en_tx_manager import *

def get_timestamp_lst(filename):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    original_filename = filename
    filename.replace("rpi_lora_lte_records_", "")
    filename = filename.replace(".csv", "")
    filename = filename.replace('-', '.')
    filename = filename.replace(':', '.')
    filename = filename.replace('T', '.')
    timestamp_lst = filename.split('.')
    timestamp_lst.append(original_filename)
    return timestamp_lst


def get_pending_files_queue(ignored_files):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    # ignored_files = []
    pending_files = []
    timestamp_lsts = []
    sorted_pending_files = []
    for filename in os.listdir(pending_dir):
        if filename in ignored_files or not filename.endswith(".csv"):
            continue
        else:
            pending_files.append(filename)
    for pending_file in pending_files:
        timestamp_lst = get_timestamp_lst(pending_file)
        timestamp_lsts.append(timestamp_lst)

    timestamp_lsts.sort()

    for lst in timestamp_lsts:
        sorted_pending_files.append(lst[-1])
    return sorted_pending_files


def send_file_to_gw(filename, compression_mode):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    send_file_to_gw_with_lora(filename, compression_mode)


def run_rx(ignored_lst, compression_mode):
    while True:
        en_stats = {}
        pending_files_queue = get_pending_files_queue(ignored_lst)
        logging.info("[{}]: The sorted pending queue is: {}".format(__name__, str(pending_files_queue)))
        for pending_file in pending_files_queue:
            if pending_file in ignored_lst:
                continue
            start = timer()
            send_file_to_gw(pending_file, compression_mode)
            end = timer()
            en_stats[pending_file] = [pending_file, os.path.getsize("{}/{}".format(pending_dir,pending_file)), end-start, compression_mode] # filename, size, start-time, TTH, compressed
            ignored_lst.append(pending_file)
        set_stats_csv(en_stats, "en_stats.csv")
        # break # TODO - remove this when we really want it to work forever. For now it's here to avoid infinite loop.
