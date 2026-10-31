import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class EncryptionError(Exception):
    """Custom exception for encryption-related errors."""
    pass


class KeyManagementError(Exception):
    """Custom exception for key management errors."""
    pass


class EncryptionHandler:
    """
    Handles encryption and decryption of sensitive data.
    """

    def __init__(self, key_file=None):
        """
        Initializes the EncryptionHandler.

        Args:
            key_file (str, optional): Path to the file containing the encryption key.
                                       If None, a new key is generated and saved to 'encryption.key'.
        """
        self.key_file = key_file or 'encryption.key'
        self.key = self._load_key()

    def _load_key(self):
        """
        Loads the encryption key from the key file.  If the file doesn't exist, generates a new key.

        Returns:
            bytes: The encryption key.

        Raises:
            KeyManagementError: If there's an error loading or generating the key.
        """
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    key = f.read()
                return key
            else:
                key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                return key
        except Exception as e:
            logging.error(f"Error loading or generating key: {e}")
            raise KeyManagementError(f"Failed to load or generate encryption key: {e}")

    def encrypt(self, data):
        """
        Encrypts the given data.

        Args:
            data (bytes): The data to encrypt.

        Returns:
            bytes: The encrypted data.

        Raises:
            EncryptionError: If there's an error during encryption.
        """
        try:
            f = Fernet(self.key)
            encrypted_data = f.encrypt(data)
            return encrypted_data
        except InvalidKey:
            logging.error("Invalid encryption key.")
            raise EncryptionError("Invalid encryption key.")
        except Exception as e:
            logging.error(f"Encryption error: {e}")
            raise EncryptionError(f"Encryption failed: {e}")

    def decrypt(self, data):
        """
        Decrypts the given data.

        Args:
            data (bytes): The data to decrypt.

        Returns:
            bytes: The decrypted data.

        Raises:
            EncryptionError: If there's an error during decryption.
        """
        try:
            f = Fernet(self.key)
            decrypted_data = f.decrypt(data)
            return decrypted_data
        except InvalidKey:
            logging.error("Invalid encryption key.")
            raise EncryptionError("Invalid encryption key.")
        except Exception as e:
            logging.error(f"Decryption error: {e}")
            raise EncryptionError(f"Decryption failed: {e}")


if __name__ == '__main__':
    # Example usage
    try:
        encryption_handler = EncryptionHandler()
        plaintext = b"This is sensitive data."
        encrypted_data = encryption_handler.encrypt(plaintext)
        print(f"Encrypted data: {encrypted_data}")
        decrypted_data = encryption_handler.decrypt(encrypted_data)
        print(f"Decrypted data: {decrypted_data}")
    except (EncryptionError, KeyManagementError) as e:
        print(f"Error: {e}")