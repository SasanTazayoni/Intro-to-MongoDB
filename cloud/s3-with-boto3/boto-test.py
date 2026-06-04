from s3_crud import list_bucket_contents, create_bucket, upload_file, delete_object, delete_bucket
from fish_market_etl import extract, transform, load

list_bucket_contents('data-eng-resources')
create_bucket('sasan-boto3-bucket')
upload_file(r'C:\Users\helpp\Desktop\test.txt', 'data-eng-resources', 'se-data-folder/test.txt')
delete_object('data-eng-resources', 'se-data-folder/test.txt')
delete_bucket('sasan-boto3-bucket')
extract('data-eng-resources', 'python/fish-market.csv', r'C:\Users\helpp\Downloads\fish-market.csv')
df = transform(r'C:\Users\helpp\Downloads\fish-market.csv')
load(df, 'data-eng-resources', 'se-data-folder/fish/sasan/fish-market-agg.csv')
