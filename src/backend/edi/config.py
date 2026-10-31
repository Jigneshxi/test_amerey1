import logging
import os

# EDI Configuration
EDI_DIRECTORY = os.getenv("EDI_DIRECTORY", "/app/edi")  # Directory where EDI files are received
ARCHIVE_DIRECTORY = os.getenv("EDI_DIRECTORY_ARCHIVE", "/app/edi/archive") # Directory to move processed files
LOG_FILE = "edi_processing.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# EDI Provider Configuration (replace with actual credentials and URLs)
EDI_PROVIDER_URL = os.getenv("EDI_PROVIDER_URL", "https://example.com/edi")
EDI_USERNAME = os.getenv("EDI_USERNAME", "your_username")
EDI_PASSWORD = os.getenv("EDI_PASSWORD", "your_password")

# Validation settings
STRICT_VALIDATION = os.getenv("STRICT_VALIDATION", "True").lower() == "true"

# Database Configuration (assuming database details are managed elsewhere - potentially via environment variables)
# You'd typically have connection strings, etc. defined here or loaded from environment variables.

# Error Notification Configuration (e.g., email settings)
ERROR_NOTIFICATION_ENABLED = os.getenv("ERROR_NOTIFICATION_ENABLED", "False").lower() == "true"
ERROR_EMAIL_RECIPIENTS = os.getenv("ERROR_EMAIL_RECIPIENTS", "errors@example.com").split(",")

# File size limit (in bytes) to prevent processing very large files.
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # Default: 10MB

def configure_logging():
    """Configures the logging system."""
    logging.info("EDI Processing Module started.")

if __name__ == '__main__':
    configure_logging()
    print(f"EDI Directory: {EDI_DIRECTORY}")
    print(f"Strict Validation: {STRICT_VALIDATION}")