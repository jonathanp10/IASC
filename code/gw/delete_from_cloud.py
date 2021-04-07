#!/usr/bin/env python3
import boto3, sys
if len(sys.argv) <= 1:
   print("ERROR: an argument <filename> is required")
   exit(1)
filename_to_delete = sys.argv[1]
s3 = boto3.resource("s3")
obj = s3.Object( "rpi-lora-lte", "raw_data/{}".format(filename_to_delete))
print("file-deleted")
