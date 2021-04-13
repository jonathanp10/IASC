import os, sys, inspect, logging, lzma

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from common.iasc_common import *
from gw.gw_tx_manager import *
from gw.cloud_status import check_success

compression_mode = True

ignore_list = []
if __name__ == "__main__":
    LOG_FILE_NAME = "iasc_gw.log"
    logging.basicConfig(filename=LOG_FILE_NAME, filemode='w', level=logging.INFO, format="%(asctime)s:%(levelname)-8s %(message)s")


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
    curr_file = open(rx_msgs[0], 'rb')
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
        logging.info("[{}][COMPRESSION_MODE:{}] bridge_dir is empty".format(__name__,str(compression_mode))
        break
    first, last, sequence_num, filename = extract_metadata(msg.split('\n')[0])
    msg_data = "\n".join(msg.split('\n')[1::])
    logging.info("[{}] msg_metadata: {} {} {} {} id {} \n".format(__name__, filename, str(first), str(last), str(sequence_num), source_id, msg_data))
    logging.debug("[{}] MsgData: {} \n".format(__name__, msg_data))
    filepath = gw_queues_dir + '/' + filename
    if first:
        curr_en_queue = open(filepath, 'wb')
        curr_en_queue.write(msg_data)
    else:
        curr_en_queue = open(filepath, 'ab+') # open in append + read mode. Reading is needed only in compression mode.
        curr_en_queue.write(msg_data)
        if last:
            if compression_mode:
                curr_en_queue.seek(0)
                compressed_data = curr_en_queue.read()
                curr_en_queue.close()
                data = lzma.decompress(compressed_data)
                curr_en_queue = open(filepath, 'wb')  # open once again the file - for overriding its compressed data with the real data
                curr_en_queue.write(data)       
            curr_en_queue.close()
            upload_to_cloud(filepath)
            if check_success(filename):
                print("Something went wrong... output file is not identical to original file.\n")


