import logging
from datetime import datetime

from src.backend.product_data.transformation import services

logger = logging.getLogger(__name__)

def transform_product_data(product_data):
    """
    Transforms raw product data into a standardized format and writes it to the Products table.

    Args:
        product_data (dict): A dictionary containing the raw product data.

    Returns:
        bool: True if the transformation and data writing were successful, False otherwise.
    """
    try:
        # Standardize data
        standardized_data = standardize_data(product_data)

        # Write to Products table
        if standardized_data:
            services.write_to_products_table(standardized_data)
            return True
        else:
            logger.error("Standardized data is empty.  Not writing to Products table.")
            return False

    except Exception as e:
        logger.error(f"Error transforming product data: {e}", exc_info=True)
        return False


def standardize_data(product_data):
    """
    Standardizes the product data dictionary.  Handles missing data and format conversions.

    Args:
        product_data (dict): The raw product data.

    Returns:
        dict: The standardized product data, or None if standardization fails.
    """
    try:
        standardized_data = {}

        # Handle required fields with defaults or error logging
        standardized_data['product_id'] = product_data.get('product_id', None)  # Keep as None if missing
        if standardized_data['product_id'] is None:
            logger.warning("Missing product_id. Skipping data.")
            return None

        standardized_data['name'] = product_data.get('name', 'Unknown Product')
        standardized_data['description'] = product_data.get('description', '')
        
        #Price - handle potential errors and format
        try:
            price = product_data.get('price')
            if price is not None:
                standardized_data['price'] = float(price)
            else:
                standardized_data['price'] = 0.0
        except (ValueError, TypeError):
            logger.error(f"Invalid price format: {product_data.get('price')}. Setting price to 0.0")
            standardized_data['price'] = 0.0

        #Category
        standardized_data['category'] = product_data.get('category', 'Uncategorized')

        #Date Handling - attempt to parse dates.  Default to current time if parsing fails.
        try:
            date_str = product_data.get('date')
            if date_str:
                standardized_data['date'] = datetime.strptime(date_str, '%Y-%m-%d')
            else:
                standardized_data['date'] = datetime.now()
        except (ValueError, TypeError):
            logger.error(f"Invalid date format: {product_data.get('date')}. Using current date.")
            standardized_data['date'] = datetime.now()

        return standardized_data

    except Exception as e:
        logger.error(f"Error standardizing data: {e}", exc_info=True)
        return None