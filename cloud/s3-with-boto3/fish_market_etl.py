import pandas as pd
from botocore.exceptions import ClientError
from s3_crud import s3_client


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
