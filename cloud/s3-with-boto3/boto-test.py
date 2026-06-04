import boto3
import pprint as pp
import pandas as pd
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def list_bucket_contents(bucket_name):
    bucket_contents = s3_client.list_objects_v2(Bucket=bucket_name)
    for object in bucket_contents['Contents']:
        print(object['Key'])


def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
        )
        print("Bucket created")
    except ClientError as e:
        print("Bucket creation failed:", e.response['Error']['Message'])


def upload_file(local_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(
            Filename=local_path,
            Bucket=bucket_name,
            Key=s3_key
        )
        print("File uploaded")
    except ClientError as e:
        print("Upload failed:", e.response['Error']['Message'])


def delete_object(bucket_name, s3_key):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
        print("Object deleted")
    except ClientError as e:
        print("Delete failed:", e.response['Error']['Message'])


def delete_bucket(bucket_name):
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print("Bucket deleted")
    except ClientError as e:
        print("Bucket deletion failed:", e.response['Error']['Message'])


list_bucket_contents('data-eng-resources')
create_bucket('sasan-boto3-bucket')
upload_file(r'C:\Users\helpp\Desktop\test.txt', 'data-eng-resources', 'se-data-folder/test.txt')
delete_object('data-eng-resources', 'se-data-folder/test.txt')
delete_bucket('sasan-boto3-bucket')
