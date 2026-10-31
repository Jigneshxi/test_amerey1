import re
from typing import Dict, List, Any

# Assuming DataValidationRules is stored securely (e.g., database)
# For simplicity, using a dictionary as a placeholder.  In a real
# application, access this from a secure data store.
DATA_VALIDATION_RULES = {}  # type: Dict[str, Dict[str, Any]]

ALLOWED_CHARACTERS = r"^[a-zA-Z0-9_.-]+$"  # Whitelist for ValidationExpression

def validate_expression(expression: str) -> bool:
    """
    Validates a ValidationExpression against a whitelist of allowed characters/patterns
    to prevent code injection.
    """
    if not re.match(ALLOWED_CHARACTERS, expression):
        return False
    return True

def load_validation_rules(rules: Dict[str, Dict[str, Any]]):
    """
    Securely loads DataValidationRules. In a production environment,
    this would involve authentication, authorization, and secure storage
    access. This is a placeholder to simulate that process.
    """
    global DATA_VALIDATION_RULES
    # In a real application, validate the rules before loading.  Check
    # for malicious patterns or attempts to bypass security measures.
    DATA_VALIDATION_RULES = rules


def validate_data(data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> List[str]:
    """
    Validates data against a set of validation rules.

    Args:
        data: The data to validate.
        rules: The validation rules.

    Returns:
        A list of error messages.  Empty list if validation succeeds.
    """

    errors = []
    for field, rule in rules.items():
        value = data.get(field)
        if value is None:
            if rule.get("required", False):
                errors.append(f"Field '{field}' is required.")
            continue

        # Apply validation rules
        validator = rule.get("validator")
        if validator:
            try:
                if not validator(value):
                    errors.append(f"Field '{field}' failed validation.")
            except Exception as e:
                errors.append(f"Error validating field '{field}': {e}")
                continue  # prevent cascading errors.

        # Type validation
        expected_type = rule.get("type")
        if expected_type:
            if expected_type == "string":
                if not isinstance(value, str):
                    errors.append(f"Field '{field}' must be a string.")
            elif expected_type == "integer":
                if not isinstance(value, int):
                    errors.append(f"Field '{field}' must be an integer.")
            elif expected_type == "float":
                if not isinstance(value, float):
                    errors.append(f"Field '{field}' must be a float.")
            elif expected_type == "boolean":
                if not isinstance(value, bool):
                    errors.append(f"Field '{field}' must be a boolean.")
            # Add more type validations as needed

        # Range validation
        min_value = rule.get("min")
        max_value = rule.get("max")
        if min_value is not None and max_value is not None:
            if not (min_value <= value <= max_value):
                errors.append(f"Field '{field}' must be between {min_value} and {max_value}.")
        elif min_value is not None:
            if value < min_value:
                errors.append(f"Field '{field}' must be greater than or equal to {min_value}.")
        elif max_value is not None:
            if value > max_value:
                errors.append(f"Field '{field}' must be less than or equal to {max_value}.")

        # Regex validation
        pattern = rule.get("pattern")
        if pattern:
            if not re.match(pattern, str(value)):
                errors.append(f"Field '{field}' does not match the required pattern.")

    return errors