import logging
from typing import List, Dict
from src.backend.product_data.transformation.transformers import transform_product_data
from src.backend.product_data.transformation.models import Product  # Assuming a Product model is defined
# Assuming MOD-005 provides database interaction functions
from src.backend.product_data.transformation import database_utils as db_utils  # Path from MOD-005

logger = logging.getLogger(__name__)

def process_product_data(raw_product_data: List[Dict]) -> None:
    """
    Processes a list of raw product data dictionaries, transforms them into a standardized format,
    and writes the standardized data to the Products table.

    Args:
        raw_product_data: A list of dictionaries, where each dictionary represents raw product data.
    """
    standardized_products: List[Product] = []
    failed_products: List[Dict] = []

    for raw_product in raw_product_data:
        try:
            standardized_product = transform_product_data(raw_product)
            if standardized_product:
                standardized_products.append(standardized_product)
            else:
                logger.warning(f"Product transformation failed for data: {raw_product}")
                failed_products.append(raw_product)
        except Exception as e:
            logger.error(f"Error transforming product data: {raw_product}. Error: {e}")
            failed_products.append(raw_product)

    if standardized_products:
        try:
            db_utils.insert_products(standardized_products)  # Use MOD-005's database utility
            logger.info(f"Successfully inserted {len(standardized_products)} products into the database.")
        except Exception as e:
            logger.error(f"Error inserting products into the database: {e}")
            # Implement data recovery mechanism here if needed, e.g., store failed products in a separate table
            logger.error(f"Failed to insert products. Consider implementing a recovery mechanism for {len(standardized_products)} products.")
    else:
        logger.warning("No products were successfully transformed.")

    if failed_products:
        logger.warning(f"Transformation failed for {len(failed_products)} products. See logs for details.")
        # Handle failed products: e.g. log them to a file or store them in a separate table for review
        # For now, just logging.  More robust handling could be implemented here.
        logger.debug(f"Failed products: {failed_products}")