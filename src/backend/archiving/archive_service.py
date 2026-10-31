import boto3
import datetime
import logging
import os
import time

from typing import List, Dict

from src.backend.archiving.config import (
    S3_BUCKET_NAME,
    ENCRYPTION_KEY,
    ACCESS_CONTROL_POLICY,
    RETENTION_DAYS
)

logger = logging.getLogger(__name__)

class ArchiveService:
    """
    Service for archiving data to S3 with encryption, access control, and integrity checks.
    """

    def __init__(self):
        self.s3_client = boto3.client('s3')

    def archive_data(self, data: List[Dict], data_source: str):
        """
        Archives a list of data dictionaries to S3.

        Args:
            data: A list of dictionaries representing the data to archive.
            data_source: A string identifying the source of the data (e.g., table name).
        """
        if not data:
            logger.info("No data to archive.")
            return

        try:
            self._upload_data_to_s3(data, data_source)
        except Exception as e:
            logger.error(f"Archival failed for {data_source}: {e}")
            self._handle_transfer_failure(data, data_source)


    def _upload_data_to_s3(self, data: List[Dict], data_source: str):
        """
        Uploads data to S3 with encryption and access control.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        object_key = f"{data_source}/{timestamp}.json"

        # Serialize data to JSON
        data_string = str(data)

        # Encrypt data
        encrypted_data = self._encrypt_data(data_string)

        # Upload to S3
        try:
            self.s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=object_key,
                Body=encrypted_data,
                ACL=ACCESS_CONTROL_POLICY,  #Enforce access control
                ServerSideEncryption='AES256' #Encryption at rest
            )
            logger.info(f"Successfully archived data from {data_source} to s3://{S3_BUCKET_NAME}/{object_key}")

            # Validate data integrity (basic check - file exists)
            self._validate_data_integrity(S3_BUCKET_NAME, object_key)

        except Exception as e:
            logger.error(f"Failed to upload data to S3: {e}")
            raise

    def _encrypt_data(self, data: str) -> bytes:
        """
        Encrypts data using a symmetric encryption key.
        """
        from cryptography.fernet import Fernet
        f = Fernet(ENCRYPTION_KEY.encode())
        encrypted_data = f.encrypt(data.encode())
        return encrypted_data

    def _validate_data_integrity(self, bucket_name: str, object_key: str):
        """
        Validates data integrity after transfer to S3.
        """
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            logger.info(f"Data integrity validation successful for s3://{bucket_name}/{object_key}")
        except Exception as e:
            logger.error(f"Data integrity validation failed: {e}")
            raise

    def _handle_transfer_failure(self, data: List[Dict], data_source: str):
        """
        Handles failed data transfers with retry mechanism and logging.
        """
        max_retries = 3
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            logger.warning(f"Retrying archival for {data_source} (attempt {attempt + 1}/{max_retries})")
            try:
                self._upload_data_to_s3(data, data_source)
                logger.info(f"Archival successful after retry for {data_source}")
                return  # Exit retry loop if successful
            except Exception as e:
                logger.error(f"Retry attempt {attempt + 1} failed: {e}")
                time.sleep(retry_delay)

        logger.error(f"Archival failed for {data_source} after {max_retries} retries.")
        #Potentially send alert here.

    def delete_old_archives(self):
        """
        Deletes archives older than the specified retention period.
        """
        retention_date = datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)
        
        #List objects in the bucket
        objects_to_delete = []
        response = self.s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified'].replace(tzinfo=None)
                if last_modified < retention_date:
                    objects_to_delete.append({'Key': obj['Key']})
        
        if objects_to_delete:
            try:
                self.s3_client.delete_objects(
                    Bucket=S3_BUCKET_NAME,
                    Delete={'Objects': objects_to_delete}
                )
                logger.info(f"Successfully deleted archives older than {retention_date}")
            except Exception as e:
                logger.error(f"Failed to delete old archives: {e}")
        else:
            logger.info("No archives to delete based on retention policy.")