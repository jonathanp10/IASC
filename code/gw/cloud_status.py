#!/usr/bin/env python3

# vim: autoindent noexpandtab tabstop=8 shiftwidth=8

import boto3
import os
import logging

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



client = boto3.client('s3')
print(client.list_objects(Bucket="rpi-lora-lte"))

print("Downloading data from cloud...")
download("rpi-lora-lte","raw_data/temperature_humidity_records_2021-03-31T19-25-38.000000.csv","temperature_humidity_records_2021-03-31T19-25-38.000000.csv.expected")

