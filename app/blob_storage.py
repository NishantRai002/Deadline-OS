"""
DeadlineOS — Azure Blob Storage helper
Author (Backend): Nishant Kumar

Provides upload_file() and get_blob_url() used by the attachment feature.
"""

import os
import uuid
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone


def _client():
    conn_str = os.getenv("AZURE_STORAGE_CONN_STR")
    if not conn_str:
        raise RuntimeError("AZURE_STORAGE_CONN_STR environment variable is not set.")
    return BlobServiceClient.from_connection_string(conn_str)


def upload_file(file_stream, original_filename: str) -> str:
    """
    Upload a file-like object to Azure Blob Storage.
    Returns the blob name (safe unique key, not a public URL).
    """
    container = os.getenv("AZURE_BLOB_CONTAINER", "attachments")
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "bin"
    blob_name = f"{uuid.uuid4().hex}.{ext}"

    client = _client()
    container_client = client.get_container_client(container)
    container_client.upload_blob(name=blob_name, data=file_stream, overwrite=True)
    return blob_name


def get_blob_url(blob_name: str, expiry_hours: int = 1) -> str:
    """
    Generate a short-lived SAS URL for a private blob.
    """
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    container = os.getenv("AZURE_BLOB_CONTAINER", "attachments")

    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(timezone.utc) + timedelta(hours=expiry_hours),
    )
    return f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
