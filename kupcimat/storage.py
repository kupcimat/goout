import datetime
import logging

from google.cloud import storage

SIGNED_URL_EXPIRATION_MINUTES = 5
FILE_SIZE_LIMIT_BYTES = 1 * 1024 * 1024


def generate_download_signed_url(bucket_name: str, blob_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        method="GET",
        expiration=datetime.timedelta(minutes=SIGNED_URL_EXPIRATION_MINUTES)
    )

    logging.info("action=generate_storage_url type=download bucket=%s blob=%s", bucket_name, blob_name)
    return url


def generate_upload_signed_url(bucket_name: str, blob_name: str) -> str:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        method="PUT",
        content_type="application/octet-stream",
        headers={"x-goog-content-length-range": f"0,{FILE_SIZE_LIMIT_BYTES}"},
        expiration=datetime.timedelta(minutes=SIGNED_URL_EXPIRATION_MINUTES)
    )

    logging.info("action=generate_storage_url type=upload bucket=%s blob=%s", bucket_name, blob_name)
    return url


def download_blob(bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    logging.info("action=download_file bucket=%s blob=%s file=%s",
                 bucket_name, source_blob_name, destination_file_name)


def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    logging.info("action=upload_file bucket=%s blob=%s file=%s",
                 bucket_name, destination_blob_name, source_file_name)


def blob_exists(bucket_name: str, blob_name: str) -> bool:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.exists()


def generate_upload_curl(url: str) -> str:
    return ("curl -X PUT "
            "-H 'Content-Type: application/octet-stream' "
            f"-H 'x-goog-content-length-range: 0,{FILE_SIZE_LIMIT_BYTES}' "
            f"--upload-file my-file '{url}'")
