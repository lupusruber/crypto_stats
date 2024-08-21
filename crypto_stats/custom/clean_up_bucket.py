if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from google.cloud import storage

def move_and_cleanup_parquet_files(bucket_name, source_folder, credentials_path, timestamp):

    storage_client = storage.Client.from_service_account_json(credentials_path)
    bucket = storage_client.bucket(bucket_name)

    destination_folder = f'{source_folder}{timestamp}/'

    blobs = bucket.list_blobs(prefix=source_folder)
    
    for blob in blobs:
        if blob.name.endswith('.parquet') and blob.name.count('/') == 1:
            new_name = blob.name.replace(source_folder, destination_folder, 1)
            new_blob = bucket.blob(new_name)
            new_blob.rewrite(blob)
            blob.delete()



@custom
def transform_custom(timestamp: int, *args, **kwargs):

    bucket_name = kwargs['bucket']
    credentials_path = kwargs['credentials_path']
    data_folder = kwargs['data_folder']

    move_and_cleanup_parquet_files(bucket_name, data_folder, credentials_path, timestamp)

