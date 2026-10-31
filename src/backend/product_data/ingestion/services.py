import logging
import boto3
from flask import jsonify, request
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# S3 configuration (replace with your actual configuration)
S3_BUCKET_NAME = "your-s3-bucket-name"
S3_REGION = "your-s3-region"

s3 = boto3.client('s3', region_name=S3_REGION)


def ingest_product_data(raw_data: str, supplier_id: str) -> Dict[str, Any]:
    """
    Ingests raw product data, validates it, sanitizes it, stores it in S3, and returns a success message.

    Args:
        raw_data (str): The raw product data.
        supplier_id (str): The ID of the data supplier.

    Returns:
        Dict[str, Any]: A dictionary containing the success message.

    Raises:
        ValueError: If the input data is invalid.
        Exception: If there is an error uploading to S3.
    """

    # Input validation
    if not raw_data or not supplier_id:
        logging.error("Invalid input: raw_data and supplier_id are required.")
        return jsonify({"message": "Invalid input format"}), 400
    
    try:
        # Sanitize raw data to prevent XSS attacks
        sanitized_data = sanitize_string(raw_data)
    except Exception as e:
        logging.error(f"Error sanitizing data: {e}")
        return jsonify({"message": "Error sanitizing data"}), 500

    # Generate a unique key for the S3 object
    s3_key = f"raw_data/{supplier_id}/{generate_unique_filename()}"

    try:
        # Upload the raw data to S3
        s3.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key, Body=sanitized_data.encode('utf-8'))
        logging.info(f"Successfully uploaded data to S3: bucket={S3_BUCKET_NAME}, key={s3_key}")
    except Exception as e:
        logging.error(f"Error uploading data to S3: {e}")
        return jsonify({"message": "S3 upload failed"}), 500
    
    return jsonify({"message": "Data accepted for processing"}), 202

def sanitize_string(input_string: str) -> str:
    """
    Sanitizes a string to prevent XSS vulnerabilities.
    This is a basic example and might need to be expanded based on the specific requirements.
    """
    # Replace HTML tags with their entities
    sanitized_string = input_string.replace("<", "&lt;").replace(">", "&gt;")
    # Remove potentially harmful characters
    sanitized_string = ''.join(c for c in sanitized_string if c.isalnum() or c in (' ', '.', '-', '_'))
    return sanitized_string

def generate_unique_filename() -> str:
    """
    Generates a unique filename using a timestamp.
    """
    import time
    return str(int(time.time())) + ".json"