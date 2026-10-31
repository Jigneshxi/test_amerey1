import json
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class MappingConfig:
    """
    Configuration class for data mapping between retailer/distributor systems and our internal model.
    """

    def __init__(self, config_path: str):
        """
        Initializes the MappingConfig with a configuration file.

        Args:
            config_path (str): Path to the JSON configuration file.
        """
        self.config_path = config_path
        self.mapping = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the mapping configuration from the JSON file.

        Returns:
            Dict[str, Any]: The loaded mapping configuration.
        
        Raises:
            FileNotFoundError: If the config file does not exist.
            json.JSONDecodeError: If the config file is invalid JSON.
        """
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self._validate_config(config)  # Validate immediately after loading
                return config
        except FileNotFoundError:
            logger.error(f"Mapping configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mapping configuration file: {self.config_path}. Error: {e}")
            raise

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validates the loaded configuration to prevent injection attacks or invalid mappings.
        Specifically checks for the presence of 'source_fields' and 'target_fields' lists
        within each mapping rule, and their data types.
        """
        if not isinstance(config, dict):
            raise ValueError("Mapping configuration must be a dictionary.")

        for source, mappings in config.items():
            if not isinstance(mappings, list):
                logger.warning(f"Invalid mapping for source {source}. Expected a list, got {type(mappings)}")
                continue #Allow config to load partially, but log warning
            for mapping_rule in mappings:
                if not isinstance(mapping_rule, dict):
                    logger.warning(f"Invalid mapping rule: {mapping_rule}. Expected a dictionary.")
                    continue
                if not all(key in mapping_rule for key in ['source_fields', 'target_fields']):
                    logger.warning(f"Missing 'source_fields' or 'target_fields' in mapping rule: {mapping_rule}")
                    continue

                if not isinstance(mapping_rule['source_fields'], list) or not isinstance(mapping_rule['target_fields'], list):
                    logger.warning(f"Invalid 'source_fields' or 'target_fields' type. Expected lists.")
                    continue

                # Basic check for potentially dangerous characters.  More thorough sanitization may be needed.
                for field in mapping_rule['source_fields'] + mapping_rule['target_fields']:
                    if not isinstance(field, str):
                        logger.warning(f"Field name is not a string: {field}")
                        continue
                    if any(char in field for char in ['<', '>', ';', "'", '"']):
                        logger.warning(f"Potentially unsafe character found in field name: {field}")


    def get_mapping(self, source_system: str) -> List[Dict[str, Any]]:
        """
        Returns the mapping configuration for a given source system.

        Args:
            source_system (str): The name of the source system.

        Returns:
            List[Dict[str, Any]]: The mapping configuration for the source system.  Returns an empty list if the source system is not found.
        """
        return self.mapping.get(source_system, [])


if __name__ == '__main__':
    # Example Usage (for testing)
    try:
        config = MappingConfig('config.json')  # Replace 'config.json' with your actual file path
        mapping = config.get_mapping('retailer_a')
        print(mapping)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")

    # Example config.json (for testing)
    # {
    #   "retailer_a": [
    #     {
    #       "source_fields": ["product_id", "product_name", "price"],
    #       "target_fields": ["sku", "name", "cost"]
    #     },
    #     {
    #       "source_fields": ["quantity"],
    #       "target_fields": ["stock_level"]
    #     }
    #   ],
    #   "distributor_b": [
    #     {
    #       "source_fields": ["item_number", "description", "unit_price"],
    #       "target_fields": ["sku", "name", "cost"]
    #     }
    #   ]
    # }