import boto3
import pprint as pp
from botocore.exceptions import NoCredentialsError, ClientError

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# --- Credential check ---
try:
    bucket_list = s3_client.list_buckets()
    print("Credentials valid. Buckets:", [b['Name'] for b in bucket_list['Buckets']])
except NoCredentialsError:
    print("No credentials found — check your ~/.aws/credentials file.")
except ClientError as e:
    print("Credentials rejected by AWS:", e.response['Error']['Message'])


# Show contents of data-eng-resources bucket:

bucket_name = 'data-eng-resources'
bucket_contents = s3_client.list_objects_v2(
  Bucket=bucket_name
  )

for object in bucket_contents['Contents']:
    print(object['Key'])
