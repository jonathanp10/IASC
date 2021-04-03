import os
import sys
from iasc_common import *
from gw_tx_manager import *
import logging
import inspect


ignore_list = []
if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_gw.log"
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")


def get_id_from_filename(filename):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    return filename.replace('./', '').split('_')[0]


def pseudo_recieve():
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    os.chdir(en_gw_bridge_dir)
    rx_msgs = filter(os.path.isfile, os.listdir('.'))
    if len(rx_msgs) == 0:
        return "__EMPTY_DIR__", -1
    rx_msgs = [os.path.join('.',f) for f in rx_msgs]
    rx_msgs.sort(key=lambda x: os.path.getmtime(x))
    # print("rx msgs:\n " + str(rx_msgs))
    curr_file = open(rx_msgs[0], 'r')
    curr_msg = curr_file.read()
    curr_file.close()
    os.remove(rx_msgs[0])
    os.chdir(working_dir)
    return curr_msg, get_id_from_filename(rx_msgs[0])


def extract_metadata(metadata):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name + "metadata is: " + metadata))
    metadata_lst = metadata.split('.csv_')
    filename = metadata_lst[0] + '.csv'
    first, last, sequence_num = metadata_lst[1].split('_')
    return first=='1', last=='1', int(sequence_num), filename


def upload_to_cloud(filepath):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name + "filepath is: " + filepath))
    send_file_to_aws(filepath)

###################################################
###################  MAIN   #######################
###################################################
logging.info("[{}] Starting run...]".format(__name__))
while True:
    # msg = recieve()
    msg, source_id = pseudo_recieve()
    if msg == "__EMPTY_DIR__":
        logging.info("[{}] bridge_dir is empty".format(__name__))
        break
    first, last, sequence_num, filename = extract_metadata(msg.split('\n')[0])
    msg_data = "\n".join(msg.split('\n')[1::])
    logging.info("[{}] msg_metadata: {} {} {} {} id {} \nmsgdata:\n {}".format(__name__, filename, str(first), str(last), str(sequence_num), source_id, msg_data))
    filepath = gw_queues_dir + '/' + filename
    if first:
        curr_en_queue = open(filepath, 'w')
        curr_en_queue.write(msg_data)
    else:
        curr_en_queue = open(filepath, 'a')
        curr_en_queue.write(msg_data)
        if last:
            curr_en_queue.close()
            upload_to_cloud(filepath)

