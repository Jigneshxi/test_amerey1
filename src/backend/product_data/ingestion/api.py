from flask import Flask, request, jsonify
import logging
import boto3
import json
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS S3 configuration (replace with your credentials and bucket name)
S3_BUCKET = os.environ.get('S3_BUCKET', 'your-s3-bucket-name')
AWS_REGION = os.environ.get('AWS_REGION', 'your-aws-region')
s3 = boto3.client('s3', region_name=AWS_REGION)

# Rate limiting (example - adjust as needed)
REQUEST_LIMIT = 10
REQUEST_WINDOW = 60  # seconds
request_counts = {}

# Helper function for rate limiting
def is_rate_limited(supplier_id):
    now = time.time()
    if supplier_id in request_counts:
        oldest_request = request_counts[supplier_id][0]
        if now - oldest_request < REQUEST_WINDOW:
            if len(request_counts[supplier_id]) >= REQUEST_LIMIT:
                return True
        # Clean up old requests
        request_counts[supplier_id] = [req_time for req_time in request_counts[supplier_id] if now - req_time < REQUEST_WINDOW]
    else:
        request_counts[supplier_id] = []
    request_counts[supplier_id].append(now)
    return False

@app.route('/products', methods=['POST'])
def ingest_product_data():
    """
    Ingests raw product data from a supplier.
    """
    if is_rate_limited(request.form.get('supplier_id')):
        logging.warning(f"Rate limit exceeded for supplier: {request.form.get('supplier_id')}")
        return jsonify({"error": "Too many requests. Please try again later."}), 429

    try:
        # Input validation
        raw_data = request.form.get('raw_data')
        supplier_id = request.form.get('supplier_id')

        if not raw_data or not supplier_id:
            logging.error("Missing required fields: raw_data or supplier_id")
            return jsonify({"error": "Missing required fields"}), 400

        # Sanitize raw_data to prevent XSS
        sanitized_data = sanitize_input(raw_data)

        # Generate a unique filename for S3 (consider using UUID)
        filename = f"{supplier_id}_{int(time.time())}.json"
        filepath = f"/tmp/{filename}"

        with open(filepath, 'w') as f:
            f.write(sanitized_data)

        # Upload to S3
        try:
            s3.upload_file(filepath, S3_BUCKET, filename)
        except Exception as e:
            logging.error(f"S3 upload failed: {e}")
            os.remove(filepath)
            return jsonify({"error": "S3 upload failed"}), 500
        finally:
            os.remove(filepath)

        logging.info(f"Data ingested from supplier {supplier_id}. File uploaded to S3: {filename}")

        return jsonify({"message": "Data accepted for processing"}), 202

    except Exception as e:
        logging.exception(f"An error occurred during data ingestion: {e}")
        return jsonify({"error": "Internal server error"}), 500

def sanitize_input(data):
    """
    Sanitizes the input string to mitigate XSS vulnerabilities.
    This is a basic example and might need to be adjusted based on the specific
    requirements and potential threats.
    """
    # Replace potentially dangerous characters with their HTML entities
    sanitized_data = data.replace("<", "&lt;").replace(">", "&gt;")
    return sanitized_data