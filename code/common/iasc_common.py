import os, logging
max_payload_len = 252
iasc_path = os.environ.get('IASC_PATH')
pending_dir = "{}/sensor_out".format(iasc_path)
en_gw_bridge_dir = "{}/en_gw_bridge".format(iasc_path)
working_dir = "{}/code".format(iasc_path)
gw_queues_dir = "{}/gw_queues".format(iasc_path)



def set_stats_csv(stats_dir, csv_name):
   stats_log = open(csv_name, 'w')
   csv_title = "filename, file size, TTH (time to handle), compression\n"
   stats_log.write(csv_title)
   logging.info(csv_title)
   for key in stats_dir:
      csv_line = "{},{},{},{}\n".format(stats_dir[key][0], stats_dir[key][1], stats_dir[key][2], stats_dir[key][3])
      stats_log.write(csv_line)
      logging.info(csv_line)
   stats_log.close()




