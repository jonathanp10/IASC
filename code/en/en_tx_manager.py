import os, sys, inspect, logging, zipfile
import time
import lzma

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *

if __name__ == "__main__":
    LOG_FILE_NAME = "en_tx_manager.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
en_id = os.environ.get('EN_ID')


def lora_pseudo_send(msg):
    logging.debug("[{}][{}][Entered function] with msg:\n {}".format(__name__, inspect.currentframe().f_code.co_name, msg))
    msg_first_line = msg.split('\n')[0]
    msg_filepath = en_gw_bridge_dir + "/" + en_id + "_" + msg_first_line
    logging.info("[{}][{}][Entered function] generating {}".format(__name__, inspect.currentframe().f_code.co_name, msg_filepath))
    if not os.path.exists(en_gw_bridge_dir):
        os.mkdir(en_gw_bridge_dir)
    msg_file = open(msg_filepath, 'wb')
    msg_file.write(msg)
    msg_file.close()
    time.sleep(0.05)


def get_metadata(filename, last, sequence_num):
    logging.debug("[{}][{}][Entered function] with [filename={}][last={}][sequence_num={}]".format(__name__, inspect.currentframe().f_code.co_name, filename, last, sequence_num))
    metadata = "{filename}_{first}_{last}_{sequence_num}\n".format(filename=filename, first=int(sequence_num == 0), last=last, sequence_num=sequence_num)
    return metadata


def send_file_to_gw_with_lora(filename, compression_mode):
    CHUNK_SIZE = 10000  #TODO: if in use - move to common module
    logging.debug("[{}][{}][Entered function] with filename: {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    sequence_num = 0
    file_path = pending_dir + "/" + filename
    file_to_send = open(file_path, 'rb')
    chunk = file_to_send.read(CHUNK_SIZE) # read first chunck of the sensor file
    while chunk:
        if compression_mode:
            chunk = lzma.compress(chunk)
        idx = 0
        while idx < len(chunk):
            payload, last = get_lora_payload(chunk,idx)  # get block in size of LoRa payload from the compressed data
            msg = get_metadata(filename, last, sequence_num) + payload
            # blocking send msg
            lora_pseudo_send(msg)
            sequence_num += 1
            idx += max_payload_len
            logging.info("[{}][{}] the msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))
        chunk = file_to_send.read(CHUNK_SIZE)
    file_to_send.close()

def get_lora_payload(data, idx):
    payload = b''
    last = 0
    
    # not last
    if idx+max_payload_len <= len(data):
        payload = data[idx:idx+max_payload_len]
    else:  # last

        payload = data[idx:]
        last = 1
    return payload, last

