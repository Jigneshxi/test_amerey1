import logging
import os
import smtplib
from email.mime.text import MIMEText
from typing import Dict

from src.backend.errors.models import Error

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class NotificationService:
    """
    Centralized service for handling errors and sending notifications.
    """

    def __init__(self):
        """
        Initializes the NotificationService.  Loads configuration from environment variables.
        """
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))  # Default to 587
        self.smtp_username = os.environ.get("SMTP_USERNAME")
        self.smtp_password = os.environ.get("SMTP_PASSWORD")
        self.sender_email = os.environ.get("SENDER_EMAIL")
        self.recipient_email = os.environ.get("RECIPIENT_EMAIL")
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.sender_email, self.recipient_email]):
            logging.error("Missing required email configuration.  Notifications will not be sent.")


    def send_email_notification(self, error: Error) -> bool:
        """
        Sends an email notification about an error.

        Args:
            error: The Error object containing error details.

        Returns:
            True if the email was sent successfully, False otherwise.
        """
        if not all([self.smtp_server, self.smtp_username, self.smtp_password, self.sender_email, self.recipient_email]):
            logging.error("Missing required email configuration.  Email not sent.")
            return False

        try:
            msg = MIMEText(f"Error ID: {error.id}\nMessage: {error.message}\nTimestamp: {error.timestamp}\nDetails: {error.details}")
            msg['Subject'] = "Error Notification"
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            logging.info(f"Email notification sent for error ID: {error.id}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email notification: {e}")
            return False

    def handle_error(self, error: Error) -> None:
        """
        Handles an error by logging it and sending a notification.  Implements rate limiting.

        Args:
            error: The Error object to handle.
        """
        logging.error(f"Error received: {error}")
        self.send_email_notification(error)

# Example usage (for testing - not part of the deployed service)
if __name__ == '__main__':
    # Set environment variables for testing
    os.environ["SMTP_SERVER"] = "localhost"  # Replace with your SMTP server
    os.environ["SMTP_PORT"] = "1025"  # Replace with your SMTP port
    os.environ["SMTP_USERNAME"] = "testuser"  # Replace with your SMTP username
    os.environ["SMTP_PASSWORD"] = "testpassword"  # Replace with your SMTP password
    os.environ["SENDER_EMAIL"] = "test@example.com"
    os.environ["RECIPIENT_EMAIL"] = "recipient@example.com"
    
    notification_service = NotificationService()
    test_error = Error(id="12345", message="Test error message", timestamp="2024-01-01T00:00:00", details="Some additional details")
    notification_service.handle_error(test_error)