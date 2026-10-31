import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def apply_rules(data: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Applies a list of predefined rules to modify data.

    Args:
        data: The data to be modified.
        rules: A list of dictionaries, where each dictionary represents a rule.
               Each rule should have a 'field', 'operation', and 'value' key.

    Returns:
        The modified data.
    """

    logger.info("Applying rules to data: %s", data)

    # Data validation before modification
    if not isinstance(data, dict):
        logger.error("Invalid input data: Data must be a dictionary.")
        raise ValueError("Input data must be a dictionary.")

    original_data = data.copy()  # Keep a copy for logging and conflict detection

    for rule in rules:
        try:
            field = rule.get('field')
            operation = rule.get('operation')
            value = rule.get('value')

            if not all([field, operation, value is not None]):
                logger.warning("Invalid rule found: %s. Skipping.", rule)
                continue

            if field not in data:
                logger.warning("Field '%s' not found in data. Skipping rule.", field)
                continue

            current_value = data[field]

            if operation == 'add':
                if isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                    data[field] = current_value + value
                elif isinstance(current_value, list) and isinstance(value, list):
                    data[field] = current_value + value
                elif isinstance(current_value, str) and isinstance(value, str):
                    data[field] = current_value + value
                else:
                    logger.error("Invalid data types for addition: %s, %s", current_value, value)
                    continue
            elif operation == 'subtract':
                if isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                    data[field] = current_value - value
                else:
                    logger.error("Invalid data types for subtraction: %s, %s", current_value, value)
                    continue
            elif operation == 'multiply':
                if isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                    data[field] = current_value * value
                else:
                    logger.error("Invalid data types for multiplication: %s, %s", current_value, value)
                    continue
            elif operation == 'divide':
                if isinstance(current_value, (int, float)) and isinstance(value, (int, float)):
                    if value == 0:
                        logger.error("Division by zero is not allowed.")
                        continue
                    data[field] = current_value / value
                else:
                    logger.error("Invalid data types for division: %s, %s", current_value, value)
                    continue
            elif operation == 'replace':
                data[field] = value
            else:
                logger.warning("Unknown operation: %s. Skipping rule.", operation)
                continue

            logger.info(f"Applied rule: {rule} to field '{field}'. New value: {data[field]}")

        except Exception as e:
            logger.error(f"Error applying rule {rule}: {e}")
            # Optionally, re-raise the exception or implement error notification

    # Data validation after modification
    if not isinstance(data, dict):
        logger.error("Data modification resulted in invalid data type.")
        raise ValueError("Data modification resulted in invalid data type.")
    
    # Conflict detection (compare original and modified data)
    if original_data != data:
        logger.info("Data modified successfully. Original data: %s, Modified data: %s", original_data, data)
    else:
        logger.info("No changes applied.")

    return data