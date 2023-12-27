from google.cloud import storage

def upload_to_bucket(blob_name, file_path, bucket_name):
    """
    Uploads a file to a Google Cloud Storage bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)

    return f"gs://{bucket_name}/{blob_name}"

