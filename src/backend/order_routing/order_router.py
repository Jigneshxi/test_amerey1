import json
import logging
from typing import Dict, Any
from flask import Flask, request, jsonify
import uuid
import time
# Assume MOD-PRODUCT-DATA-MANAGEMENT provides a function to check inventory
# and get fulfillment center locations.  Replace with actual import when
# that module is generated.
# from mod_product_data_management import check_inventory, get_fulfillment_centers

# Mock functions for demonstration purposes.  Remove these when
# integrating with the actual module.
def check_inventory(product_id: str, fulfillment_center: str, quantity: int) -> bool:
    """Mocks checking inventory at a fulfillment center."""
    # Simulate some inventory levels
    inventory = {
        "FC1": {"A123": 100, "B456": 50},
        "FC2": {"A123": 20, "B456": 80},
        "FC3": {"A123": 75, "B456": 25}
    }
    if fulfillment_center in inventory and product_id in inventory[fulfillment_center]:
        return inventory[fulfillment_center][product_id] >= quantity
    return False

def get_fulfillment_centers(customer_location: str) -> list[Dict[str, Any]]:
    """Mocks getting fulfillment center locations and distances."""
    # Simulate fulfillment center locations and distances
    fulfillment_centers = [
        {"name": "FC1", "location": "New York", "distance": 100},
        {"name": "FC2", "location": "Los Angeles", "distance": 200},
        {"name": "FC3", "location": "Chicago", "distance": 150}
    ]
    #Filter based on customer location to reduce the number of fulfillment centers to evaluate
    filtered_centers = []
    for center in fulfillment_centers:
        if center["location"] == customer_location or customer_location == "Any":
            filtered_centers.append(center)
    return filtered_centers


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/orders', methods=['POST'])
def route_order():
    """
    API endpoint to route incoming orders to the appropriate fulfillment center.
    """
    try:
        data = request.get_json()
        quantity = data['quantity']
        product_id = data['product_id']
        customer_location = data['customer_location']

        if not all([quantity, product_id, customer_location]):
            return jsonify({"error": "Invalid input"}), 400

        fulfillment_centers = get_fulfillment_centers(customer_location)

        # Find the closest fulfillment center with available inventory
        closest_center = None
        min_distance = float('inf')
        
        for center in fulfillment_centers:
            if check_inventory(product_id, center['name'], quantity):
                if center['distance'] < min_distance:
                    min_distance = center['distance']
                    closest_center = center
                elif center['distance'] == min_distance and closest_center is not None:
                    # Handle multiple fulfillment centers with equal distance and inventory.
                    # For simplicity, choose the first one.  Could implement more sophisticated logic.
                    pass
        
        if closest_center is None:
            logging.error(f"Routing failed for order: {product_id}, quantity: {quantity}, location: {customer_location}")
            #Retry logic (example: retry 3 times with exponential backoff)
            for attempt in range(3):
                time.sleep(2**attempt)  # Exponential backoff
                fulfillment_centers = get_fulfillment_centers(customer_location) #refresh centers
                closest_center = None
                min_distance = float('inf')
                for center in fulfillment_centers:
                    if check_inventory(product_id, center['name'], quantity):
                        if center['distance'] < min_distance:
                            min_distance = center['distance']
                            closest_center = center
                        elif center['distance'] == min_distance and closest_center is not None:
                            pass #handle equal distance
                if closest_center is not None:
                    break

            if closest_center is None:
                return jsonify({"error": "Routing failure"}), 500
            
        order_id = str(uuid.uuid4())
        
        #In a production system, this would be a call to a separate order management system
        # to create the order and associate it with the fulfillment center.
        
        response = {
            "order_id": order_id,
            "fulfillment_center": closest_center['name']
        }
        
        logging.info(f"Order {order_id} routed to {closest_center['name']}")
        return jsonify(response), 202

    except Exception as e:
        logging.exception(f"An error occurred during order routing: {e}")
        return jsonify({"error": "Routing failure"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)