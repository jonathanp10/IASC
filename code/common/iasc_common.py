import os, logging
max_payload_len =  252
max_metadata_flags_len = 9 # 1 first, 1 last, 3 sequence + seperators + \n
en_sleep_time_in_sec = 5
gw_sleep_time_in_sec = 10
iasc_path = os.environ.get('IASC_PATH')
pending_dir = "{}/sensor_out".format(iasc_path)
en_gw_bridge_dir = "{}/en_gw_bridge".format(iasc_path)
working_dir = "{}/code".format(iasc_path)
gw_queues_dir = "{}/gw_queues".format(iasc_path)
gw_dir = "{}/{}".format(working_dir, "gw")
gw_downloads = "{}/{}".format(gw_dir, "downloads")
gw_stats_path = "{}/{}".format(gw_dir, "gw_stats.csv")



def init_stats_csv(csv_name):
   stats_log = open(csv_name, 'w')
   csv_title = "filename, file size, TTH (time to handle), compression\n"
   stats_log.write(csv_title)
   stats_log.close()



def set_stats_csv(stats_dict, csv_name):
   stats_log = open(csv_name, 'a')
   #logging.info(csv_title)
   for key in stats_dict:
      csv_line = "{},{},{},{}\n".format(stats_dict[key][0], stats_dict[key][1], stats_dict[key][2], stats_dict[key][3])
      stats_log.write(csv_line)
      #logging.info(csv_line)
   stats_log.close()




