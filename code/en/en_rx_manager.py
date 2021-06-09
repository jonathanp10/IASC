import os, sys, inspect, logging, argparse
from timeit import default_timer as timer
import time
import busio
from digitalio import DigitalInOut
import board
import adafruit_rfm9x

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
from en.en_tx_manager import *
from gw.gw_tx_manager import upload_to_cloud

def get_timestamp_lst(filename):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    original_filename = filename
    filename.replace(DATA_FILE_PREFIX, "")
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


def send_file_to_gw(filename, compression_mode, rfm9x=None):
    logging.debug("[{}][{}][Entered function] filename is {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    return send_file_to_gw_with_lora(filename, compression_mode, rfm9x)


def run_rx(ignored_lst, compression_mode, sim_mode=False):
    if not sim_mode:
        # configure LoRa module
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        try:
            rfm9x = adafruit_rfm9x.RFM9x(spi,CS,RESET,LoRa_FREQ)
            rfm9x.node = EN_ID
            rfm9x.destination = GW_NODE_ID
            rfm9x.ack_retries = ACK_RETRIES
            rfm9x.ack_delay = ACK_DELAY
            rfm9x.enable_crc = LORA_ENABLE_CRC
            logging.info("[{}]: Configured LoRa".format(__name__))
        except RuntimeError as error:
            print("ERROR: Please check LoRa-RPi wiring\n")
            logging.info("[{}]: ERROR: Failed to initialize RFM9X object. Probably wiring issue\n".format(__name__,))
            return False # TODO: some exit code?
            
    while True:
        en_stats = {}
        pending_files_queue = get_pending_files_queue(ignored_lst)
        if len(pending_files_queue) == 0:
            logging.info("[{}]: The sorted pending queue is empty\nGoing to sleep for {} sec".format(__name__, en_sleep_time_in_sec))
            print("EN {}: Empty dir. sleeping...".format(en_id))
            time.sleep(en_sleep_time_in_sec)
        else:
            logging.info("[{}]: The sorted pending queue is: {}".format(__name__, str(pending_files_queue)))
        for pending_file in pending_files_queue:
            if pending_file in ignored_lst:
                continue
            start = time.time() #timer()
            if CELLULAR_EN_MODE:
                upload_to_cloud(pending_dir + "/" + pending_file)
            elif sim_mode:  # simulation mode - don't pass rfm9x object.
                send_file_to_gw(pending_file, compression_mode)
            else:  # regular LoRa transmission
                practical_lora_tth = send_file_to_gw(pending_file, compression_mode, rfm9x)
            end = timer()
            en_stats[pending_file] = [pending_file, os.path.getsize("{}/{}".format(pending_dir,pending_file)), start, compression_mode, practical_lora_tth] # filename, size, start-time, TTH, compressed
            ignored_lst.append(pending_file)
            set_stats_csv(en_stats, "en_stats.csv")
        
