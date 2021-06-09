import os, sys, inspect, logging, zipfile, adafruit_rfm9x
import time
import lzma
from timeit import default_timer as timer

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
    msg_first_line = msg.decode('utf-8').split('\n')[0]
    msg_filepath = en_gw_bridge_dir + "/" + en_id + "_" + msg_first_line + "_NOT_READY"
    logging.info("[{}][{}][Entered function] generating {}".format(__name__, inspect.currentframe().f_code.co_name, msg_filepath))
    if not os.path.exists(en_gw_bridge_dir):
        os.mkdir(en_gw_bridge_dir)
    msg_file = open(msg_filepath, 'wb')
    msg_file.write(msg)
    msg_file.close()
    os.rename(msg_filepath, msg_filepath.replace("_NOT_READY",""))
    time.sleep(0.05)


def get_metadata(filename, last, sequence_num):
    logging.debug("[{}][{}][Entered function] with [filename={}][last={}][sequence_num={}]".format(__name__, inspect.currentframe().f_code.co_name, filename, last, sequence_num))
    metadata = "{filename}_{first}_{last}_{sequence_num}\n".format(filename=filename, first=int(sequence_num == 0), last=last, sequence_num=sequence_num)
    return metadata


def send_file_to_gw_with_lora(filename, compression_mode, rfm9x=None):
    practical_lora_tth = 0
    logging.debug("[{}][{}][Entered function] with filename: {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    sequence_num = 0
    file_path = pending_dir + "/" + filename
    file_to_send = open(file_path, 'rb')
    compressed_size = 0

    data = file_to_send.read()
    file_to_send.close()
    if compression_mode:
        data = lzma.compress(data)
        compressed_size += len(data)
    idx = 0
    while idx < len(data):
        payload, last = get_lora_payload(data,idx,filename)  # get block in size of LoRa payload from the compressed data. If it's the last payload in the chunk - returns last = 1
        metadata = bytes(get_metadata(filename, last, sequence_num), 'utf-8')
        #print("metadata length: {}\n Metadata is {}".format(len(metadata), metadata))
        msg = metadata + payload
        # blocking send msg
        if rfm9x == None:
            lora_pseudo_send(msg)
        else:
            #print("MSG LENGTH: {}".format(len(msg)))
            #print(msg)
            start = timer()
            rfm9x.send_with_ack(msg)
            end = timer()
            practical_lora_tth += end-start
        sequence_num += 1
        max_payload_len_without_metadata = max_payload_len - max_metadata_flags_len - len(filename)
        idx += max_payload_len_without_metadata 
        logging.info("[{}][{}] the msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))
    return practical_lora_tth

def get_lora_payload(data, idx, filename):
    payload = b''
    last = 0
    max_payload_len_without_metadata = max_payload_len - max_metadata_flags_len - len(filename)
    # not last
    if idx+max_payload_len_without_metadata <= len(data):
        payload = data[idx:idx+max_payload_len_without_metadata]
    else:  # last
        payload = data[idx:]
        last = 1
    return payload, last

