import os, logging, argparse
iasc_path = os.environ.get('IASC_PATH')
pending_dir = "{}/sensor_out".format(iasc_path)
en_gw_bridge_dir = "{}/en_gw_bridge".format(iasc_path)
working_dir = "{}/code".format(iasc_path)
gw_queues_dir = "{}/gw_queues".format(iasc_path)
gw_dir = "{}/{}".format(working_dir, "gw")
gw_downloads = "{}/{}".format(gw_dir, "downloads")
gw_stats_path = "{}/{}".format(gw_dir, "gw_stats.csv")
DATA_FILE_PREFIX = "iasc"


# LoRa Configuration
LoRa_FREQ = 915.0
ACK_RETRIES = 100
ACK_DELAY = 0.1
LORA_RECEIVE_TIMEOUT = 1000
GW_NODE_ID = 10
LORA_ENABLE_CRC = True
EN_ID = int(os.environ.get('EN_ID'))

# System Configuration
max_payload_len =  251
max_metadata_flags_len = 9 # 1 first, 1 last, 3 sequence + seperators + \n
en_sleep_time_in_sec = 5
gw_sleep_time_in_sec = 10
cleaner_sleep_time_in_sec = 1800 # 0.5 hour
CELLULAR_EN_MODE = False



def init_stats_csv(csv_name):
   stats_log = open(csv_name, 'w')
   csv_title = "filename, file size, TTH (time to handle), compression\n"
   stats_log.write(csv_title)
   stats_log.close()



def set_stats_csv(stats_dict, csv_name):
   stats_log = open(csv_name, 'a')
   #logging.info(csv_title)
   for key in stats_dict:
      csv_line = "{},{},{},{}\n".format(stats_dict[key][0], stats_dict[key][1], stats_dict[key][2], stats_dict[key][3])#, stats_dict[key][4])
      stats_log.write(csv_line)
      #logging.info(csv_line)
   stats_log.close()

def parse_args(args): 
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-dbg', '-debug', dest='dbg', action="store_true", required=False, help = "Open logger in debug mode")
    arg_parser.add_argument('-sim', action="store_true", required=False, help = "Start up application in simulation mode")
    arg_parser.add_argument('-comp', '-compression', dest='comp', required=False, action = "store_true", help = "in this mode en compress all tx files")
    #arg_parser.add_argument('-compression', required=False, action = "store_true", help = "in this mode en compress all tx files")
    parsed_args = arg_parser.parse_args(args)
    return parsed_args





