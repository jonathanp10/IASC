import os, sys, inspect, logging, zipfile
import time

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *

if __name__ == "__main__":
    LOG_FILE_NAME = "en_tx_manager.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
en_id = os.environ.get('EN_ID')


def lora_pseudo_send(msg, compression_mode):
    logging.debug("[{}][{}][Entered function] with msg:\n {}".format(__name__, inspect.currentframe().f_code.co_name, msg))
    msg_first_line = msg.split('\n')[0]
    msg_filepath = en_gw_bridge_dir + "/" + en_id + "_" + msg_first_line
    logging.info("[{}][{}][Entered function] generating {}".format(__name__, inspect.currentframe().f_code.co_name, msg_filepath))
    if not os.path.exists(en_gw_bridge_dir):
        os.mkdir(en_gw_bridge_dir)
    if compression_mode:
        msg_file = open(msg_filepath, 'wb')
    else:
        msg_file = open(msg_filepath, 'w')
    msg_file.write(msg)
    msg_file.close()
    time.sleep(0.05)


def get_metadata(filename, last, sequence_num):
    logging.debug("[{}][{}][Entered function] with [filename={}][last={}][sequence_num={}]".format(__name__, inspect.currentframe().f_code.co_name, filename, last, sequence_num))
    metadata = "{filename}_{first}_{last}_{sequence_num}\n".format(filename=filename, first=int(sequence_num == 0), last=last, sequence_num=sequence_num)
    return metadata



def send_file_to_gw_with_lora(filename, compression_mode):
    logging.debug("[{}][{}][Entered function] with filename: {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    sequence_num = 0
    file_path = pending_dir + "/" + filename
    if compression_mode:
        with zipfile.ZipFile("{}.zip".format(file_path), 'w', compression=zipfile.ZIP_DEFLATED) as zip_to_send:
            zip_to_send.write(file_path)
        file_to_send = open("{}.zip".format(file_path), 'rb')
        logging.info("[{}][{}][Compressing...] TEXT FILE: {}\nZI FILE: {}".format(__name__, inspect.currentframe().f_code.co_name, file_path, os.path.abspath(file_to_send.name)))
    else:
        file_to_send = open(file_path, 'r')
    payload = ""
    for line in file_to_send:
        line_length = len(line)
        if len(payload) + line_length <= max_payload_len:
            payload += line
        else:
            msg = get_metadata(filename, 0, sequence_num) + payload
            # blocking send msg
            lora_pseudo_send(msg, compression_mode)
            sequence_num += 1
            logging.info("[{}][{}] the msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))
            payload = line # init payload
    file_to_send.close()
    msg = get_metadata(filename, 1, sequence_num) + payload
    # send msg
    lora_pseudo_send(msg, compression_mode)
    logging.info("[{}][{}] the LAST msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))



