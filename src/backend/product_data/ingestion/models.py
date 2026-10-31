import uuid
from datetime import datetime
from typing import Optional
import re

class ProductData:
    """
    Represents the raw product data ingested from various suppliers.
    """

    def __init__(self, raw_data: str, supplier_id: str, s3_key: Optional[str] = None, created_at: Optional[datetime] = None, data_id: Optional[str] = None):
        """
        Initializes a ProductData object.

        Args:
            raw_data: The raw product data string.
            supplier_id: The ID of the supplier providing the data.
            s3_key: The S3 key where the raw data is stored.
            created_at: The timestamp when the data was ingested.
            data_id: Unique ID for the data
        """
        self.raw_data = self._validate_and_sanitize_raw_data(raw_data)
        self.supplier_id = self._validate_supplier_id(supplier_id)
        self.s3_key = s3_key
        self.created_at = created_at if created_at else datetime.utcnow()
        self.data_id = data_id if data_id else str(uuid.uuid4())

    def _validate_and_sanitize_raw_data(self, raw_data: str) -> str:
        """
        Validates and sanitizes the raw data to prevent injection attacks and XSS vulnerabilities.

        Args:
            raw_data: The raw data string.

        Returns:
            The sanitized raw data string.

        Raises:
            TypeError: If raw_data is not a string.
        """
        if not isinstance(raw_data, str):
            raise TypeError("Raw data must be a string.")

        # Sanitize: Remove potentially harmful characters.  This is a basic example,
        # more robust sanitization might be required depending on the expected data format.
        sanitized_data = re.sub(r'[<>&"]', '', raw_data)
        return sanitized_data

    def _validate_supplier_id(self, supplier_id: str) -> str:
        """
        Validates the supplier ID.

        Args:
            supplier_id: The supplier ID string.

        Returns:
            The validated supplier ID string.

        Raises:
            TypeError: If supplier_id is not a string.
            ValueError: If supplier_id is empty.
        """
        if not isinstance(supplier_id, str):
            raise TypeError("Supplier ID must be a string.")
        if not supplier_id:
            raise ValueError("Supplier ID cannot be empty.")
        return supplier_id

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the ProductData object.
        """
        return {
            "data_id": self.data_id,
            "raw_data": self.raw_data,
            "supplier_id": self.supplier_id,
            "s3_key": self.s3_key,
            "created_at": self.created_at.isoformat()
        }