import logging
from datetime import datetime

# Assuming a database interaction layer exists elsewhere.  For now, using a simple in-memory store for demonstration.
# In a production environment, this would interact with a database.
class VersionService:
    """
    Provides version control for product data.
    """

    def __init__(self):
        self.versions = {}  # {product_id: {version: {data: {}, timestamp: datetime}}}
        self.logger = logging.getLogger(__name__)

    def create_version(self, product_id, data):
        """
        Creates a new version of the product data.

        Args:
            product_id (str): The ID of the product.
            data (dict): The product data.

        Returns:
            int: The new version number.  Returns -1 on error.
        """
        try:
            if product_id not in self.versions:
                self.versions[product_id] = {}
                version = 1
            else:
                version = max(self.versions[product_id].keys()) + 1

            self.versions[product_id][version] = {
                'data': data,
                'timestamp': datetime.utcnow()
            }
            self.logger.info(f"Created version {version} for product {product_id}")
            return version

        except Exception as e:
            self.logger.error(f"Error creating version for product {product_id}: {e}")
            return -1

    def get_version(self, product_id, version):
        """
        Retrieves a specific version of the product data.

        Args:
            product_id (str): The ID of the product.
            version (int): The version number.

        Returns:
            dict: The product data for the specified version, or None if not found.
        """
        if product_id in self.versions and version in self.versions[product_id]:
            return self.versions[product_id][version]['data']
        else:
            self.logger.warning(f"Version {version} not found for product {product_id}")
            return None

    def get_latest_version(self, product_id):
        """
        Retrieves the latest version of the product data.

        Args:
            product_id (str): The ID of the product.

        Returns:
            dict: The latest product data, or None if not found.
        """
        if product_id in self.versions:
            latest_version = max(self.versions[product_id].keys())
            return self.versions[product_id][latest_version]['data']
        else:
            self.logger.warning(f"Product {product_id} not found")
            return None

    def rollback_to_version(self, product_id, version):
        """
        Rolls back the product data to a specific version.  This effectively
        makes the specified version the 'current' version by updating any
        references or data structures that rely on the latest version.

        Args:
            product_id (str): The ID of the product.
            version (int): The version number to roll back to.

        Returns:
            bool: True if the rollback was successful, False otherwise.
        """
        try:
            if product_id in self.versions and version in self.versions[product_id]:
                # In a real system, this would involve updating the 'current'
                # pointer to this version, and potentially invalidating other versions.
                # For this example, we just log the rollback.

                # Find the highest version, and 'delete' all versions above the target version
                highest_version = max(self.versions[product_id].keys())
                for v in range(version + 1, highest_version + 1):
                    del self.versions[product_id][v]

                self.logger.info(f"Rolled back product {product_id} to version {version}")
                return True
            else:
                self.logger.warning(f"Rollback to version {version} failed for product {product_id}. Version not found.")
                return False

        except Exception as e:
            self.logger.error(f"Error rolling back product {product_id} to version {version}: {e}")
            return False