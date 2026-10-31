import time
import logging
from typing import Dict, Any

from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redis configuration (for rate limiting and potentially caching)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Notification credentials (securely stored - e.g., environment variables or a secrets manager)
# In a real application, do NOT hardcode credentials.  Use environment variables or a secrets manager.
EMAIL_API_KEY = os.environ.get('EMAIL_API_KEY')
SMS_API_KEY = os.environ.get('SMS_API_KEY')

# Rate limiting settings
MAX_NOTIFICATIONS_PER_MINUTE = 100
RATE_LIMIT_WINDOW = 60  # seconds

def send_notification(user_id: str, message: str, channel: str) -> bool:
    """
    Sends a notification to a user via the specified channel.

    Args:
        user_id: The ID of the user to notify.
        message: The notification message.
        channel: The notification channel (e.g., "email", "sms").

    Returns:
        True if the notification was sent successfully, False otherwise.
    """
    try:
        if channel == "email":
            # Replace with actual email sending logic using EMAIL_API_KEY
            # Example:
            # smtp = smtplib.SMTP('smtp.example.com', 587)
            # smtp.starttls()
            # smtp.login("your_email", EMAIL_API_KEY)
            # smtp.sendmail("sender@example.com", user_id, message)
            logging.info(f"Sending email to {user_id}: {message}")
            return True
        elif channel == "sms":
            # Replace with actual SMS sending logic using SMS_API_KEY
            # Example:
            # twilio_client = Client(SMS_API_KEY)
            # message = twilio_client.messages.create(
            #     to=user_id,
            #     from_="+15558675309",
            #     body=message
            # )
            logging.info(f"Sending SMS to {user_id}: {message}")
            return True
        else:
            logging.error(f"Unsupported notification channel: {channel}")
            return False
    except Exception as e:
        logging.error(f"Error sending notification to {user_id} via {channel}: {e}")
        return False

def is_rate_limited(user_id: str) -> bool:
    """
    Checks if a user has exceeded the rate limit for notifications.

    Args:
        user_id: The ID of the user.

    Returns:
        True if the user is rate limited, False otherwise.
    """
    key = f"notifications:{user_id}"
    count = redis_client.get(key)
    if count is None:
        redis_client.set(key, 1, ex=RATE_LIMIT_WINDOW)
        return False
    else:
        count = int(count)
        if count >= MAX_NOTIFICATIONS_PER_MINUTE:
            return True
        else:
            redis_client.incr(key, 1)
            return False

@app.route('/errors', methods=['POST'])
def handle_error():
    """
    Handles error notifications.
    """
    try:
        data = request.get_json()
        message = data.get('message')
        severity = data.get('severity')

        if not message or not severity:
            return jsonify({"error": "Invalid input"}), 400

        # Example usage: Send an email to the system administrator
        admin_user_id = "admin@example.com"  # Replace with actual admin user ID
        notification_message = f"Error: {message}\nSeverity: {severity}"

        if not is_rate_limited(admin_user_id):
            if send_notification(admin_user_id, notification_message, "email"):
                logging.info(f"Error notification sent to admin: {message}")
                return jsonify({}), 204
            else:
                logging.error(f"Failed to send error notification to admin: {message}")
                return jsonify({"error": "Failed to send notification"}), 500
        else:
            logging.warning(f"Rate limited for admin user: {admin_user_id}")
            return jsonify({"error": "Rate limited"}), 429

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)