#!/usr/bin/env python3

# vim: autoindent noexpandtab tabstop=8 shiftwidth=8

import boto3
import os, sys, inspect,logging

# modify PYTHONPATH in order to imprt internal modules from parent directory.
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.iasc_common import *
 

LOG_FILE_NAME = "cloud_gw_download.log"
if __name__ == "__main__":
   logging.basicConfig(filename = LOG_FILE_NAME, filemode='w', level = logging.INFO, format = "%(asctime)s:%(levelname)-8s %(message)s")
   client = boto3.client('s3')
   print(client.list_objects(Bucket="rpi-lora-lte"))
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)



def download(bucket_name, server_file_path, output_path):
   logging.debug("Downloading {server_file_path} from bucket {bucket_name} to {output_path}...".format(server_file_path = server_file_path, bucket_name = bucket_name, output_path = output_path))
   s3 = boto3.resource('s3')
   try:
      s3.meta.client.download_file(bucket_name, server_file_path, output_path)
      logging.debug("File downloaded successfully.")
   except Exception as e:
      logging.error("Error occurred in downloading file.")
      logging.error(e)
        

def check_success(filename, source_id): # return True for failure, False for success
    # download file from cloud
    server_file_path = "raw_data/" + filename + "_" + source_id
    output_path = filename + "_" + source_id + ".expected"
    download("rpi-lora-lte",server_file_path,output_path)
    
    # path to original file
    original_file_path = pending_dir + "/" + filename
    
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
    os.remove(output_path)
    return False
    
    

#print("Downloading data from cloud...")

# test check_success function.
#check_success("temperature_humidity_records_2021-04-05T14-59-14.344970.csv")



