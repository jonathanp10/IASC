import os, sys, inspect, logging, lzma, adafruit_rfm9x
import time
import busio
import board
from digitalio import DigitalInOut
from timeit import default_timer as timer
from queue import Queue as Queue

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


def lora_receive(rfm9x):
    msg = rfm9x.receive(with_ack=True, with_header=True, timeout=5000)
    if msg is None: 
       print("Packet is None")
       return lora_receive(rfm9x)
    else:
       msg_str = msg[4:].decode('utf-8', 'ignore')
       #print("Packet is: {}".format(msg_str))
       #print("Header: {} ".format(str([hex(x) for x in msg[0:4]])))
    return msg[4::], str(msg[1])

def pseudo_recieve():
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    os.chdir(en_gw_bridge_dir)
    rx_msgs = list(filter(os.path.isfile, os.listdir('.')))
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
    if DATA_FILE_PREFIX not in str(curr_msg, 'utf-8'):
        print("[pseudo_receive] pseudo recieve illegal msg" + curr_msg[:60])
        print("[pseudo_receive] ILLEGAL: " + rx_msgs[0])
        exit(2)
    os.remove(rx_msgs[0])
    os.chdir(gw_dir)
    return curr_msg, get_id_from_filename(rx_msgs[0])


def extract_metadata(metadata):
    #print("BEFORE CONVERTING TO STR: {}".format(metadata))
    try:
       metadata = str(metadata, 'utf-8')
    except UnicodeDecodeError:
      #print("Error occured decoding metadata - ignoring packet")
      logging.info("[{}][{}] Error occured decoding metadata - ignoring packet".format(__name__, inspect.currentframe().f_code.co_name ))
      return False, False, -1, "__DROPPED_PACKET__"
      #exit(1)

    #print("AFTER CONVERTING TO STR: {}".format(metadata))
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name ))
    metadata_lst = metadata.split('.csv_')
    filename = metadata_lst[0] + '.csv'
    # print(metadata_lst)
    first, last, sequence_num = metadata_lst[1].split('_')
    return first=='1', last=='1', int(sequence_num), filename

    
def handle_msgs(rx_fifo, ignored_lst, compression_mode):
    queues_dict = {}
    cnt = 0
    logging.info("[{}] msg handler awake".format(__name__))
    while True:
        if rx_fifo.empty():  # no msgs are waiting - go to sleep
            logging.info("[{}][{}] rx_fifo is empty, going to sleep for {} sec".format(__name__, inspect.currentframe().f_code.co_name, gw_sleep_time_in_sec))
            print("RX_FIFO EMPTY, going to sleep...")
            time.sleep(gw_sleep_time_in_sec)
        else:
            msg, source_id = rx_fifo.get() 
            logging.info("[{}][{}] Handling msg from EN {}".format(__name__,inspect.currentframe().f_code.co_name, source_id))
            metadata = msg.split(b'\n')[0]
#print("Metadata: {}".format(metadata))
            logging.info("[{}][{}] Metadata: {}".format(__name__,inspect.currentframe().f_code.co_name, metadata))
            first, last, sequence_num, filename = extract_metadata(metadata)
            if filename == "__DROPPED_PACKET__":
               continue
            msg_data = b'\n'.join(msg.split(b'\n')[1::])
            logging.info("[{}][{}] msg_metadata: {} {} {} {} id {} \n".format(__name__,inspect.currentframe().f_code.co_name, filename, str(first), str(last), str(sequence_num), source_id, msg_data))
            logging.debug("[{}] MsgData: {} \n".format(__name__, msg_data))
            filepath = "{}/{}_{}".format(gw_queues_dir, filename, source_id)
#print("Filpath: " + filepath)

            # first msg - create new file
            if first:
                curr_en_queue = open(filepath, 'wb+')
                queues_dict[filepath] = curr_en_queue
            queues_dict[filepath].write(msg_data)
            # last msg - close file and upload to cloud
            if last:
                start = 0 #timer() 
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
                end = time.time()
                cnt +=1
                print("GW uploaded {} files".format(str(cnt)))
                append_gw_stats(filename + "_" + source_id, end-start, compression_mode) # filename, size, start-time, TTH, compressed
                #if check_success(filename, source_id):
                #    print("Something went wrong... output file is not identical to original file.\n")
                #else:
                #    print(filename + " UPLOAD PERFECTLY MATCH :) ")
               

def append_gw_stats(filename, tth, compression_mode): 
    gw_stats = open(gw_stats_path, 'a')
    filesize = os.path.getsize("{}/{}".format(gw_queues_dir,filename))
    csv_line = "{},{},{},{}\n".format(filename, filesize, tth, compression_mode)
    gw_stats.write(csv_line)
    logging.info("[{}][{}] STATS_LINE: {}".format(__name__,inspect.currentframe().f_code.co_name, csv_line))
    gw_stats.close()


def run_rx(rx_fifo, sim_mode=False):
    logging.info("[{}] rx manager is awake".format(__name__))
    if not sim_mode:
        # Configure LoRa radio
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, LoRa_FREQ)
        rfm9x.node = GW_NODE_ID
        rfm9x.enable_crc = LORA_ENABLE_CRC
        rfm9x.receive_timeout = LORA_RECEIVE_TIMEOUT
        rfm9x.ack_delay = ACK_DELAY
        logging.info("[{}] Configured Lora".format(__name__))
    while True:
        if sim_mode:
            msg, source_id = pseudo_recieve()
        else:
            msg, source_id = lora_receive(rfm9x)
        # print("RUN_RX Entered 50 chars: {}".format(msg[:50]))
        if msg == "__EMPTY_DIR__":
            logging.info("[{}] bridge_dir is empty".format(__name__))
            time.sleep(gw_sleep_time_in_sec)
            print("gw_finished")
        else:
            rx_fifo.put((msg,source_id))
