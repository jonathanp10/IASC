import os
import sys
from iasc_common import *
import time
import logging
import inspect

if __name__ == "__main__":
    LOG_FILE_NAME = "en_tx_manager.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")
en_id = os.environ.get('EN_ID')


def lora_pseudo_send(msg):
    logging.debug("[{}][{}][Entered function] with msg:\n {}".format(__name__, inspect.currentframe().f_code.co_name, msg))
    msg_first_line = msg.split('\n')[0]
    msg_filepath = en_gw_bridge_dir + "/" + en_id + "_" + msg_first_line
    logging.info("[{}][{}][Entered function] generating {}".format(__name__, inspect.currentframe().f_code.co_name, msg_filepath))
    msg_file = open(msg_filepath, 'w')
    msg_file.write(msg)
    msg_file.close()
    time.sleep(0.05)


def get_metadata(filename, last, sequence_num):
    logging.debug("[{}][{}][Entered function] with [filename={}][last={}][sequence_num={}]".format(__name__, inspect.currentframe().f_code.co_name, filename, last, sequence_num))
    metadata = "{filename}_{first}_{last}_{sequence_num}\n".format(filename=filename, first=int(sequence_num == 0), last=last, sequence_num=sequence_num)
    return metadata



def send_file_to_gw_with_lora(filename):
    logging.debug("[{}][{}][Entered function] with filename: {}".format(__name__, inspect.currentframe().f_code.co_name, filename))
    sequence_num = 0
    file_path = pending_dir + "/" + filename
    file_to_send = open(file_path, 'r')
    payload = ""
    for line in file_to_send:
        line_length = len(line)
        if len(payload) + line_length <= max_payload_len:
            payload += line
        else:
            msg = get_metadata(filename, 0, sequence_num) + payload
            # blocking send msg
            lora_pseudo_send(msg)
            sequence_num += 1
            logging.info("[{}][{}] the msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))
            payload = line # init payload
    file_to_send.close()
    msg = get_metadata(filename, 1, sequence_num) + payload
    # send msg
    lora_pseudo_send(msg)
    logging.info("[{}][{}] the LAST msg that is sent:\n{}".format(__name__, inspect.currentframe().f_code.co_name, msg))



