import os
from typing import Optional

class ArchivingConfig:
    """
    Configuration settings for the data archiving module.
    """

    def __init__(self):
        # S3 configuration
        self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
        if not self.s3_bucket_name:
            raise ValueError("S3_BUCKET_NAME not set in environment variables")

        self.s3_region = os.environ.get("S3_REGION", "us-east-1")  # Default region

        # Encryption settings (at rest)
        self.encryption_enabled = os.environ.get("ENCRYPTION_ENABLED", "True").lower() == "true"
        self.kms_key_id = os.environ.get("KMS_KEY_ID")
        if self.encryption_enabled and not self.kms_key_id:
            raise ValueError("KMS_KEY_ID must be set if encryption is enabled")

        # Access control settings
        self.access_control_policy = os.environ.get("ACCESS_CONTROL_POLICY", "private") # Default to private

        # Retention policy (in days)
        self.retention_days = int(os.environ.get("RETENTION_DAYS", "30"))  # Default to 30 days

        # Data integrity validation
        self.validate_data_integrity = os.environ.get("VALIDATE_DATA_INTEGRITY", "True").lower() == "true"

        # Retry settings
        self.max_retries = int(os.environ.get("MAX_RETRIES", "3"))
        self.retry_delay = int(os.environ.get("RETRY_DELAY", "5")) #seconds

        # Logging settings
        self.log_level = os.environ.get("LOG_LEVEL", "INFO") #INFO, WARNING, ERROR
        self.log_file = os.environ.get("LOG_FILE", "archiving.log")


    def get_s3_bucket_name(self) -> str:
        return self.s3_bucket_name

    def get_s3_region(self) -> str:
        return self.s3_region
    
    def is_encryption_enabled(self) -> bool:
        return self.encryption_enabled

    def get_kms_key_id(self) -> Optional[str]:
        return self.kms_key_id

    def get_access_control_policy(self) -> str:
        return self.access_control_policy
    
    def get_retention_days(self) -> int:
        return self.retention_days
    
    def should_validate_data_integrity(self) -> bool:
        return self.validate_data_integrity
    
    def get_max_retries(self) -> int:
        return self.max_retries
    
    def get_retry_delay(self) -> int:
        return self.retry_delay
    
    def get_log_level(self) -> str:
        return self.log_level

    def get_log_file(self) -> str:
        return self.log_file

# Example usage (for testing/local development)
if __name__ == "__main__":
    config = ArchivingConfig()
    print(f"S3 Bucket Name: {config.get_s3_bucket_name()}")
    print(f"Encryption Enabled: {config.is_encryption_enabled()}")
    print(f"Retention Days: {config.get_retention_days()}")