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


def extract(bucket_name, s3_key, local_path):
    try:
        s3_client.download_file(Bucket=bucket_name, Key=s3_key, Filename=local_path)
        print("File downloaded")
    except ClientError as e:
        print("Download failed:", e.response['Error']['Message'])


def transform(local_path):
    df = pd.read_csv(local_path, encoding='utf-8-sig')
    aggregated = df.groupby('Species')[['Weight', 'Length1', 'Length2', 'Length3', 'Height', 'Width']].mean()
    print(aggregated)
    return aggregated


def load(df, bucket_name, s3_key):
    from io import StringIO
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
        print(f"Loaded to s3://{bucket_name}/{s3_key}")
    except ClientError as e:
        print("Load failed:", e.response['Error']['Message'])


list_bucket_contents('data-eng-resources')
create_bucket('sasan-boto3-bucket')
upload_file(r'C:\Users\helpp\Desktop\test.txt', 'data-eng-resources', 'se-data-folder/test.txt')
delete_object('data-eng-resources', 'se-data-folder/test.txt')
delete_bucket('sasan-boto3-bucket')
extract('data-eng-resources', 'python/fish-market.csv', r'C:\Users\helpp\Downloads\fish-market.csv')
df = transform(r'C:\Users\helpp\Downloads\fish-market.csv')
load(df, 'data-eng-resources', 'se-data-folder/fish/sasan/fish-market-agg.csv')
