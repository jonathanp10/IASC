import os
max_payload_len = 252
iasc_path = os.environ.get('IASC_PATH')
pending_dir = "{}/sensor_out".format(iasc_path)
en_gw_bridge_dir = "{}/en_gw_bridge".format(iasc_path)
working_dir = "{}/code".format(iasc_path)
gw_queues_dir = "{}/gw_queues".format(iasc_path)
