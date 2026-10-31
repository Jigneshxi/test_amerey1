from flask import Flask, request, jsonify
import logging
import uuid
from src.backend.errors.notification_service import send_error_notification

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/errors", methods=["POST"])
def report_error():
    """
    API endpoint to report errors.
    Logs the error and sends a notification.
    """
    try:
        data = request.get_json()
        error_message = data.get("message")

        if not error_message:
            return jsonify({"error": "Error message is required"}), 400

        error_id = str(uuid.uuid4())

        # Log the error
        logging.error(f"Error ID: {error_id}, Message: {error_message}")

        # Send notification (using notification service)
        send_error_notification(error_id, error_message)

        return jsonify({"id": error_id}), 200

    except Exception as e:
        logging.exception("An unexpected error occurred in /errors endpoint")
        return jsonify({"error": "Internal server error"}), 500