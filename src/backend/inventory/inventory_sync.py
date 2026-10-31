import logging
from flask import Flask, jsonify, request
from flask.views import MethodView
import threading
import time
from src.backend.inventory.models import Inventory
from src.backend.inventory.models import InventoryHistory

# Assuming MOD-PRODUCT-DATA-MANAGEMENT provides a way to check product existence
# For demonstration, we'll mock it.  In a real system, this would be an import.
def product_exists(product_id):
    """Mock function to check if a product exists."""
    # In a real implementation, this would call a function in the
    # MOD-PRODUCT-DATA-MANAGEMENT module.
    return True

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global lock for optimistic locking
inventory_lock = threading.Lock()

class InventorySync(MethodView):
    def get(self, productId):
        """
        Retrieves the current inventory level for a given product.
        """
        try:
            if not product_exists(productId):
                return jsonify({'message': 'Product not found'}), 404

            inventory = Inventory.query.filter_by(product_id=productId).first()

            if inventory is None:
                return jsonify({'inventory_level': 0}), 200 # Or potentially create a new inventory entry

            return jsonify({'inventory_level': inventory.level}), 200

        except Exception as e:
            logging.error(f"Error getting inventory for product {productId}: {e}")
            return jsonify({'message': 'Internal server error'}), 500

    def put(self, productId):
        """
        Updates the inventory level for a given product.  This is likely not needed,
        as updates would originate from the fulfillment centers.  Included for completeness.
        """
        try:
            if not product_exists(productId):
                return jsonify({'message': 'Product not found'}), 404

            data = request.get_json()
            new_level = data.get('inventory_level')

            if new_level is None:
                return jsonify({'message': 'Inventory level missing'}), 400

            inventory = Inventory.query.filter_by(product_id=productId).first()

            if inventory is None:
                inventory = Inventory(product_id=productId, level=new_level)
                db.session.add(inventory)
            else:
                inventory.level = new_level

            db.session.commit()
            self._log_inventory_change(productId, inventory.level, new_level) # Log the change

            return jsonify({'message': 'Inventory updated successfully'}), 200

        except Exception as e:
            logging.error(f"Error updating inventory for product {productId}: {e}")
            return jsonify({'message': 'Internal server error'}), 500


    def _log_inventory_change(self, product_id, old_level, new_level):
        """Logs inventory changes for auditing."""
        history_entry = InventoryHistory(
            product_id=product_id,
            old_level=old_level,
            new_level=new_level,
            timestamp=time.time()
        )
        db.session.add(history_entry)
        db.session.commit()
        logging.info(f"Inventory changed for product {product_id}: from {old_level} to {new_level}")

    def _check_discrepancy(self, product_id, expected_level, actual_level):
        """Alerts operations team on significant inventory discrepancies."""
        if abs(expected_level - actual_level) > 10:  # Example threshold
            logging.warning(f"Significant inventory discrepancy for product {product_id}: Expected {expected_level}, Actual {actual_level}")
            # In a real system, this would trigger an alert to the operations team
            # e.g., via email, Slack, or a monitoring system.


# This function would be triggered by events from fulfillment centers.
def update_inventory(product_id, quantity_change):
    """
    Updates the inventory level for a given product, handling concurrency and logging.
    """
    try:
        if not product_exists(product_id):
            logging.error(f"Product {product_id} does not exist.")
            return

        with inventory_lock:
            inventory = Inventory.query.filter_by(product_id=product_id).first()
            if inventory is None:
                inventory = Inventory(product_id=product_id, level=quantity_change)
            else:
                old_level = inventory.level
                new_level = inventory.level + quantity_change
                if new_level < 0:
                    logging.error(f"Attempted to reduce inventory below zero for product {product_id}.")
                    # Handle overselling - e.g., reject the update, or raise an exception.
                    return # Prevent overselling
                inventory.level = new_level
                self._check_discrepancy(product_id, old_level, new_level)
            db.session.commit()
            self._log_inventory_change(product_id, inventory.level - quantity_change, inventory.level)


    except Exception as e:
        logging.error(f"Error updating inventory for product {product_id}: {e}")

app.add_url_rule('/products/<string:productId>', view_func=InventorySync.as_view('inventory_sync'))

if __name__ == '__main__':
    from src.backend.inventory.models import db
    db.create_all()  # Create database tables
    app.run(debug=True)