from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Inventory(models.Model):
    product_id = models.IntegerField(unique=True)  # Foreign key to Product model in MOD-PRODUCT-DATA-MANAGEMENT
    inventory_level = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)  # For optimistic locking

    class Meta:
        indexes = (
            models.Index(fields=['product_id']),
        )

    def __str__(self):
        return f"Inventory for Product ID: {self.product_id}, Level: {self.inventory_level}, Version: {self.version}"

    def update_inventory(self, new_level):
        """
        Updates inventory level with optimistic locking.
        Returns True if update was successful, False otherwise.
        """
        try:
            # Attempt to update only if the version matches the current version in the database.
            Inventory.objects.filter(product_id=self.product_id, version=self.version).update(
                inventory_level=new_level,
                version=self.version + 1
            )

            # Log the inventory change
            logger.info(f"Inventory updated for product {self.product_id}: from {self.inventory_level} to {new_level}. Version: {self.version}")
            return True

        except Exception as e:
            # Handle optimistic locking conflicts or other errors
            logger.error(f"Failed to update inventory for product {self.product_id}: {e}")
            return False

    def check_overselling(self, quantity):
        """
        Checks if selling the given quantity would result in overselling.
        Returns True if overselling would occur, False otherwise.
        """
        return self.inventory_level < quantity

    @staticmethod
    def alert_discrepancy(product_id, expected_level, actual_level):
        """
        Alerts the operations team on significant inventory discrepancies.
        """
        discrepancy_percentage = abs(expected_level - actual_level) / expected_level if expected_level else 0
        if discrepancy_percentage > 0.1:  # 10% discrepancy threshold
            logger.warning(f"Significant inventory discrepancy for product {product_id}: Expected {expected_level}, Actual {actual_level}. Percentage difference: {discrepancy_percentage:.2f}")
            # TODO: Implement actual alerting mechanism (e.g., email, Slack notification)
            print(f"ALERT: Inventory discrepancy for product {product_id}") # Placeholder for now