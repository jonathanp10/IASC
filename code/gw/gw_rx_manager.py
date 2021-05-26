import os, sys, inspect, logging, lzma
from timeit import default_timer as timer
from queue import Queue as Queue
import time

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from common.iasc_common import *
from gw.gw_tx_manager import *
from gw.cloud_status import check_success

def get_id_from_filename(filename):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    return filename.replace('./', '').split('_')[0]


def pseudo_recieve():
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    os.chdir(en_gw_bridge_dir)
    rx_msgs = filter(os.path.isfile, os.listdir('.'))
    logging.debug("[{}][{}] rx msgs is: {}".format(__name__, inspect.currentframe().f_code.co_name, str(rx_msgs)))
    for msg in rx_msgs:
      if "NOT_READY" in msg:
         rx_msgs.remove(msg)
    if len(list(rx_msgs)) == 0:
        return "__EMPTY_DIR__", -1
    rx_msgs = [os.path.join('.',f) for f in rx_msgs]
    rx_msgs.sort(key=lambda x: os.path.getmtime(x))
    # print("rx msgs:\n " + str(rx_msgs))
    curr_file = open(rx_msgs[0], 'rb')
    curr_msg = curr_file.read()
    curr_file.close()
    if "rpi_lora_lte" not in curr_msg:
        print("[pseudo_receive] pseudo recieve illegal msg" + curr_msg[:60])
        print("[pseudo_receive] ILLEGAL: " + rx_msgs[0])
        exit(2)
    os.remove(rx_msgs[0])
    os.chdir(gw_dir)
    return curr_msg, get_id_from_filename(rx_msgs[0])


def extract_metadata(metadata):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name + "metadata is: " + metadata))
    metadata_lst = metadata.split('.csv_')
    filename = metadata_lst[0] + '.csv'
    # print(metadata_lst)
    first, last, sequence_num = metadata_lst[1].split('_')
    return first=='1', last=='1', int(sequence_num), filename

    
def handle_msgs(rx_fifo, ignored_lst, compression_mode):
    queues_dict = {}
    logging.info("[{}] msg handler awake".format(__name__))
    while True:
        if rx_fifo.empty():  # no msgs are waiting - go to sleep
            logging.info("[{}] rx_fifo is empty, going to sleep for {} sec".format(__name__, gw_sleep_time_in_sec))
            time.sleep(gw_sleep_time_in_sec)
        else:
            msg, source_id = rx_fifo.get() 
            # print("HANDLER:\n" + msg[:60])
            first, last, sequence_num, filename = extract_metadata(msg.split('\n')[0])
            msg_data = "\n".join(msg.split('\n')[1::])
            logging.info("[{}] msg_metadata: {} {} {} {} id {} \n".format(__name__, filename, str(first), str(last), str(sequence_num), source_id, msg_data))
            logging.debug("[{}] MsgData: {} \n".format(__name__, msg_data))
            filepath = "{}/{}_{}".format(gw_queues_dir, filename, source_id)

            # first msg - create new file
            if first:
                curr_en_queue = open(filepath, 'wb+')
                queues_dict[filepath] = curr_en_queue
            queues_dict[filepath].write(msg_data)
            # last msg - close file and upload to cloud
            if last:
                start = timer() 
                if compression_mode:
                    queues_dict[filepath].seek(0)
                    compressed_data = queues_dict[filepath].read()
                    data = lzma.decompress(compressed_data)
                    queues_dict[filepath].seek(0)
                    queues_dict[filepath].write(data)
                # logging.info("[{}] GW_QUEUES: {}".format(__name__, queues_dict[filepath].read()))
                queues_dict[filepath].close()
                upload_to_cloud(filepath)
                queues_dict.pop(filepath)
                ignored_lst.append("{}_{}".format(filename, source_id))
                end = timer()
                append_gw_stats(filename + "_" + source_id, end-start, compression_mode) # filename, size, start-time, TTH, compressed
                if check_success(filename, source_id):
                    print("Something went wrong... output file is not identical to original file.\n")
                else:
                    print(filename + " UPLOAD PERFECTLY MATCH :) ")


def append_gw_stats(filename, tth, compression_mode): 
    gw_stats = open(gw_stats_path, 'a')
    filesize = os.path.getsize("{}/{}".format(gw_queues_dir,filename))
    csv_line = "{},{},{},{}\n".format(filename, filesize, tth, compression_mode)
    gw_stats.write(csv_line)
    logging.info("[{}] STATS_LINE: {}".format(__name__, csv_line))
    gw_stats.close()


def run_rx(rx_fifo):
    logging.info("[{}] rx manager is awake".format(__name__))
    while True:
        # msg = recieve()
        msg, source_id = pseudo_recieve()
        # print("RUN_RX Entered 50 chars: {}".format(msg[:50]))
        if msg == "__EMPTY_DIR__":
            logging.info("[{}] bridge_dir is empty".format(__name__))
            time.sleep(gw_sleep_time_in_sec)
            # break
        else:
            rx_fifo.put((msg,source_id))
