#!/usr/bin/env python3

# vim: autoindent noexpandtab tabstop=8 shiftwidth=8

import boto3, os, sys, logging, inspect
# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *


if __name__ == "__main__":
	LOG_FILE_NAME = "gw_tx_manager.log"
	logging.basicConfig(filename=LOG_FILE_NAME, level = logging.INFO, format = "%(asctime)s:%(levelname)-8s %(message)s")
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

def upload(file_basename, bucket_name, server_file_path):
	logging.debug("Uploading {file_basename} to bucket {bucket_name} as {server_file_path}".format(file_basename = file_basename, bucket_name = bucket_name, server_file_path = server_file_path))
	s3 = boto3.resource('s3')
	try:
		s3.meta.client.upload_file(file_basename, bucket_name, server_file_path)
		logging.debug("File uploaded successfully.")
	except Exception as e:
		logging.error("Error occurred in uploading file.")
		logging.error(e)


def send_file_to_aws(filepath):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name))
    logging.info("[{}][{}] uploading {}...".format(__name__, inspect.currentframe().f_code.co_name, filepath))
    upload(os.path.abspath(filepath), "rpi-lora-lte", "raw_data/{}".format(os.path.basename(filepath)))


def upload_to_cloud(filepath):
    logging.debug("[{}][{}][Entered function]".format(__name__, inspect.currentframe().f_code.co_name + "filepath is: " + filepath))
    send_file_to_aws(filepath)
