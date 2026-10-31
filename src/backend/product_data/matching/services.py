import logging
from django.db import transaction
from .models import ProductMatching

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.8  # Adjust as needed

def match_products(product1, product2):
    """
    Matches two products based on their attributes.

    Args:
        product1: The first product (represented as a dictionary or object).
        product2: The second product (represented as a dictionary or object).

    Returns:
        True if the products are considered a match, False otherwise.
    """
    try:
        # Implement a more sophisticated matching algorithm here.
        # This is a placeholder for a real implementation.
        # Consider using techniques like string similarity, feature vectors, etc.
        similarity_score = calculate_similarity(product1, product2)

        if similarity_score >= CONFIDENCE_THRESHOLD:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error during product matching: {e}")
        return False

def calculate_similarity(product1, product2):
    """
    Calculates a similarity score between two products.
    This is a placeholder and should be replaced with a robust similarity calculation.
    """
    # Example: Compare name and category (very basic)
    score = 0.0
    if product1.get('name') and product2.get('name') and product1['name'].lower() == product2['name'].lower():
        score += 0.5
    if product1.get('category') and product2.get('category') and product1['category'].lower() == product2['category'].lower():
        score += 0.5
    return score

def deduplicate_products(products):
    """
    Deduplicates a list of products.

    Args:
        products: A list of product dictionaries or objects.

    Returns:
        A list of unique products, with matching information stored in the ProductMatching table.
    """
    unique_products = []
    matched_pairs = []

    for i in range(len(products)):
        product1 = products[i]
        for j in range(i + 1, len(products)):
            product2 = products[j]
            if match_products(product1, product2):
                # Log the match
                logger.info(f"Matched products: {product1.get('id')} and {product2.get('id')}")
                matched_pairs.append((product1, product2))

                # Store matching information (using transaction for atomicity)
                with transaction.atomic():
                    try:
                        matching = ProductMatching.objects.create(
                            product1_id=product1.get('id'),
                            product2_id=product2.get('id'),
                            confidence_score=calculate_similarity(product1, product2)
                        )
                        matching.save()
                    except Exception as e:
                        logger.error(f"Error saving product matching: {e}")
                break  # Only match each product once

        unique_products.append(product1)

    return unique_products

def review_matches():
    """
    Provides a mechanism for reviewing and correcting matches.
    (This could involve a UI or a batch processing script).
    """
    # Implement a way to view potential matches and manually confirm or reject them.
    # This is a placeholder for a more comprehensive review process.
    matches = ProductMatching.objects.all()
    for match in matches:
        print(f"Reviewing match: Product1 ID={match.product1_id}, Product2 ID={match.product2_id}, Confidence={match.confidence_score}")
        # Add UI or script for manual review and correction here.
    pass