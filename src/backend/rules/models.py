from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Rule:
    """
    Represents a rule for data modification.
    """
    def __init__(self, name: str, condition: callable, action: callable):
        """
        Initializes a Rule object.

        Args:
            name (str): The name of the rule.
            condition (callable): A function that checks if the rule should be applied.  Should return True or False.
            action (callable): A function that performs the data modification.
        """
        self.name = name
        self.condition = condition
        self.action = action

    def apply(self, data: Any) -> Any:
        """
        Applies the rule to the given data.

        Args:
            data (Any): The data to modify.

        Returns:
            Any: The modified data.
        """
        try:
            if self.condition(data):
                logger.info(f"Applying rule: {self.name}")
                
                # Data Validation before modification
                if not self.validate_data_before(data):
                    logger.error(f"Data validation failed before applying rule {self.name}. Data: {data}")
                    raise ValueError(f"Data validation failed before applying rule {self.name}")

                modified_data = self.action(data)

                # Data Validation after modification
                if not self.validate_data_after(modified_data):
                    logger.error(f"Data validation failed after applying rule {self.name}. Modified Data: {modified_data}")
                    raise ValueError(f"Data validation failed after applying rule {self.name}")

                logger.info(f"Rule {self.name} applied successfully.")
                return modified_data
            else:
                logger.debug(f"Rule {self.name} condition not met. Skipping.")
                return data
        except Exception as e:
            logger.error(f"Error applying rule {self.name}: {e}")
            raise

    def validate_data_before(self, data: Any) -> bool:
        """
        Validates the data before modification.  Override this method in subclasses
        for specific validation needs.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        return True  # Default: Always valid

    def validate_data_after(self, data: Any) -> bool:
        """
        Validates the data after modification. Override this method in subclasses
        for specific validation needs.

        Args:
            data (Any): The data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        return True # Default: Always valid


class RuleEngine:
    """
    Applies a list of rules to data.
    """
    def __init__(self, rules: List[Rule]):
        """
        Initializes a RuleEngine object.

        Args:
            rules (List[Rule]): A list of Rule objects to apply.
        """
        self.rules = rules

    def apply_rules(self, data: Any) -> Any:
        """
        Applies all rules to the given data.

        Args:
            data (Any): The data to modify.

        Returns:
            Any: The modified data.
        """
        modified_data = data
        for rule in self.rules:
            modified_data = rule.apply(modified_data)
        return modified_data