from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FulfillmentCenter:
    def __init__(self, center_id: str, location: str, capacity: int):
        self.center_id = center_id
        self.location = location
        self.capacity = capacity
        self.current_inventory = 0

    def available_capacity(self) -> int:
        return self.capacity - self.current_inventory

    def __repr__(self):
        return f"FulfillmentCenter(id={self.center_id}, location={self.location}, capacity={self.capacity}, inventory={self.current_inventory})"


class Order:
    def __init__(self, order_id: str, product_id: str, quantity: int, customer_location: str):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.customer_location = customer_location

    def __repr__(self):
        return f"Order(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, location={self.customer_location})"


class RoutingResult:
    def __init__(self, order_id: str, fulfillment_center_id: str):
        self.order_id = order_id
        self.fulfillment_center_id = fulfillment_center_id

    def __repr__(self):
        return f"RoutingResult(order_id={self.order_id}, fulfillment_center_id={self.fulfillment_center_id})"

class OrderRoutingError(Exception):
    """Custom exception for order routing failures."""
    pass

def calculate_distance(location1: str, location2: str) -> float:
    """
    Placeholder for distance calculation logic.
    In a real application, this would use a map API or other distance calculation method.
    For simplicity, this returns a random value between 0 and 100.
    """
    # In a production system, use a proper distance calculation method
    import random
    return random.uniform(0, 100)

def find_best_fulfillment_center(order: Order, fulfillment_centers: List[FulfillmentCenter]) -> Optional[FulfillmentCenter]:
    """
    Finds the best fulfillment center for a given order based on distance and inventory.
    """
    closest_center = None
    min_distance = float('inf')

    for center in fulfillment_centers:
        if center.available_capacity() >= order.quantity:
            distance = calculate_distance(order.customer_location, center.location)
            if distance < min_distance:
                min_distance = distance
                closest_center = center
            elif distance == min_distance and closest_center:
                # Handle edge case: Multiple fulfillment centers with equal distance and inventory.
                # Prioritize the center with lower ID.
                if int(center.center_id) < int(closest_center.center_id):
                    closest_center = center

    return closest_center