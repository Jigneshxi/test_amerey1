import time
import random
from typing import Dict, Optional

from src.backend.product_data.models import ProductAttributes  # Assuming models are defined elsewhere
from src.backend.product_data.enrichment.exceptions import EnrichmentServiceUnavailableError, RateLimitExceededError

# Dependency on MOD-006 (replace with actual import if available)
# Assuming MOD-006 provides a function to fetch data.
# from mod_006 import fetch_product_details

def enrich_product_data(product_id: str) -> Optional[ProductAttributes]:
    """
    Enriches product data with information from external sources.

    Args:
        product_id: The ID of the product to enrich.

    Returns:
        A ProductAttributes object with enriched data, or None if enrichment fails.
    """

    try:
        enriched_data = _fetch_from_external_service(product_id)
        if enriched_data:
            # Create or update ProductAttributes
            product_attributes, created = ProductAttributes.objects.get_or_create(
                product_id=product_id,
                defaults={
                    "additional_details": enriched_data
                }
            )
            if not created:
                product_attributes.additional_details = enriched_data
                product_attributes.save()
            return product_attributes
        else:
            print(f"No enrichment data found for product ID: {product_id}")
            return None

    except EnrichmentServiceUnavailableError:
        print(f"Enrichment service unavailable for product ID: {product_id}. Using fallback.")
        # Implement fallback mechanism (e.g., use cached data, return default values)
        return _get_default_product_attributes(product_id)
    except RateLimitExceededError:
        print(f"Rate limit exceeded for product ID: {product_id}. Retrying after delay.")
        _handle_rate_limit()
        return enrich_product_data(product_id)  # Retry after delay
    except Exception as e:
        print(f"An unexpected error occurred while enriching product data for ID {product_id}: {e}")
        return None


def _fetch_from_external_service(product_id: str) -> Optional[Dict]:
    """
    Fetches product details from an external service (MOD-006).

    Args:
        product_id: The ID of the product.

    Returns:
        A dictionary containing enriched data, or None if unavailable.

    Raises:
        EnrichmentServiceUnavailableError: If the external service is unavailable.
        RateLimitExceededError: If the rate limit is exceeded.
    """
    # Simulate external service call with potential errors
    if random.random() < 0.1:  # 10% chance of service being unavailable
        raise EnrichmentServiceUnavailableError("External service is currently unavailable.")
    if random.random() < 0.05:  # 5% chance of rate limit being exceeded
        raise RateLimitExceededError("Rate limit exceeded.")

    # Replace with actual call to MOD-006
    # try:
    #     enriched_data = fetch_product_details(product_id)
    #     return enriched_data
    # except Exception as e:
    #     print(f"Error fetching data from MOD-006: {e}")
    #     return None

    # Simulate enriched data for testing
    enriched_data = {"color": "blue", "material": "cotton", "size": "large"}
    return enriched_data


def _get_default_product_attributes(product_id: str) -> ProductAttributes:
    """
    Returns default product attributes as a fallback.

    Args:
        product_id: The ID of the product.

    Returns:
        A ProductAttributes object with default values.
    """
    return ProductAttributes(product_id=product_id, additional_details={})


def _handle_rate_limit():
    """
    Handles rate limits by waiting for a certain period.
    """
    wait_time = 60  # seconds
    print(f"Waiting {wait_time} seconds to avoid rate limit.")
    time.sleep(wait_time)