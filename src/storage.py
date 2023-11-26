from google.cloud import storage

GCS_BUCKET_NAME = 'expenselens_input'

storage_client = storage.Client()

def upload_to_gcs(file_path, destination_blob_name):
    bucket = storage_client.get_bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
