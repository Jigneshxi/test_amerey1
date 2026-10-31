import csv
import io
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def parse_csv_data(csv_file_content: str, schema: Dict[str, type]) -> List[Dict[str, Any]]:
    """
    Parses CSV data from a string and validates it against a schema.

    Args:
        csv_file_content: The content of the CSV file as a string.
        schema: A dictionary defining the expected data types for each column. 
                Example: {'column1': str, 'column2': int, 'column3': float}

    Returns:
        A list of dictionaries, where each dictionary represents a row of data.
        Returns an empty list if parsing fails.
    
    Raises:
        TypeError: if schema is not a dict
    """

    if not isinstance(schema, dict):
        raise TypeError("Schema must be a dictionary.")
    
    data = []
    try:
        csvfile = io.StringIO(csv_file_content)
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            validated_row = {}
            is_valid = True
            for column, value in row.items():
                if column not in schema:
                    logger.warning(f"Column '{column}' not found in schema. Skipping.")
                    continue

                expected_type = schema[column]
                
                # Sanitize data
                sanitized_value = sanitize_data(value)

                try:
                    if expected_type == int:
                        validated_value = int(sanitized_value)
                    elif expected_type == float:
                        validated_value = float(sanitized_value)
                    elif expected_type == bool:
                        validated_value = sanitized_value.lower() == 'true'
                    else:
                        validated_value = str(sanitized_value)  # Convert to string by default
                except ValueError:
                    logger.error(f"Invalid data type for column '{column}'. Expected {expected_type}, got {type(sanitized_value)}.")
                    is_valid = False
                    break
                validated_row[column] = validated_value

            if is_valid:
                data.append(validated_row)

    except csv.Error as e:
        logger.error(f"CSV parsing error: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

    return data

def sanitize_data(value: str) -> str:
    """
    Sanitizes a string value to prevent CSV injection attacks.
    
    Args:
        value: The string to sanitize.
    
    Returns:
        The sanitized string.
    """
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Escape double quotes by doubling them
    value = value.replace('"', '""')
    
    # Prevent formula injection (e.g., start with '=')
    if value.startswith('='):
        value = "'" + value
    
    return value
    
if __name__ == '__main__':
    # Example Usage
    csv_data = """
    name,age,city
    John Doe,30,New York
    Jane Smith,25,London
    Peter Jones,40,Paris
    """

    schema = {'name': str, 'age': int, 'city': str}

    parsed_data = parse_csv_data(csv_data, schema)
    print(parsed_data)

    #Example with invalid data
    csv_data_invalid = """
    name,age,city
    John Doe,abc,New York
    """
    parsed_data_invalid = parse_csv_data(csv_data_invalid, schema)
    print(parsed_data_invalid)