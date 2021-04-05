#!/usr/bin/env python3

# vim: autoindent noexpandtab tabstop=8 shiftwidth=8

import boto3
import os
import logging
from common.iasc_common import *
 

LOG_FILE_NAME = "cloud_gw_download.log"
logging.basicConfig(filename = LOG_FILE_NAME, level = logging.INFO, format = "%(asctime)s:%(levelname)-8s %(message)s")
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def download_timings_file():
	download("si7021-temperature-humidity-sensor", "config_files/timings.ini", "timings.ini")


def download(bucket_name, server_file_path, output_path):
	logging.debug("Downloading {server_file_path} from bucket {bucket_name} to {output_path}...".format(server_file_path = server_file_path, bucket_name = bucket_name, output_path = output_path))
	s3 = boto3.resource('s3')
	try:
		s3.meta.client.download_file(bucket_name, server_file_path, output_path)
		logging.debug("File downloaded successfully.")
	except Exception as e:
		logging.error("Error occurred in downloading file.")
		logging.error(e)
        
def check_success(filename): # return True for failure, False for success
    # download file from cloud
    server_file_path = "raw_data/" + filename
    output_path = filename + ".expected"
    download("rpi-lora-lte",server_file_path,output_path)
    
    # path to original file
    original_file_path = pending_dir + "/filename"
    
    # first test - compare size
    if os.path.getsize(output_path) != os.path.getsize(original_file_path):
        logging.error("FAILURE: Size mismatch between original file ({original_size}) and file downloaded from server ({output_size}).\n".format(original_size=os.path.getsize(original_file_path), output_size=os.path.getsize(output_path)))
        return True
        
    # Second test - diff files
    with open(original_file_path, 'r') as original_file:
        with open(output_path, 'r') as output:
            difference = set(original_file).difference(output)
            if len(difference) > 0:
                logging.error("FAILURE: {diff_num} differences were found between original and output files: {differences}\n".format(diff_num=len(difference), differences=str(difference)))
                return True
    logging.info("Original file and output file perfectly match!")
    return False
    
    
client = boto3.client('s3')
print(client.list_objects(Bucket="rpi-lora-lte"))

print("Downloading data from cloud...")
download("rpi-lora-lte","raw_data/temperature_humidity_records_2021-03-31T19-25-38.000000.csv","temperature_humidity_records_2021-03-31T19-25-38.000000.csv.expected")

