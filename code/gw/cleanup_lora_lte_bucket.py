#!/usr/bin/env python3
import boto3, sys

s3 = boto3.resource('s3')
s3.Bucket("rpi-lora-lte").objects.filter(Prefix='raw_data/').delete()
