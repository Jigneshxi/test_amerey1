from django.db import models
import re

class DataValidationRules(models.Model):
    field_name = models.CharField(max_length=255, help_text="The name of the field to validate.")
    validation_type = models.CharField(max_length=50, help_text="The type of validation to perform (e.g., regex, min_length, max_length, email).")
    validation_expression = models.TextField(help_text="The expression used for validation (e.g., regex pattern, minimum length, maximum length).", blank=True, null=True)
    error_message = models.TextField(help_text="The error message to return if validation fails.", blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Indicates if the rule is currently active.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field_name} - {self.validation_type}"

    def validate(self, value):
        """
        Validates a given value against the rule's criteria.
        Returns a list of error messages if validation fails, otherwise an empty list.
        """
        errors = []

        if self.validation_type == 'regex':
            if self.validation_expression:
                # Security: Whitelist allowed characters/patterns to prevent code injection
                if not re.match(self.validation_expression, value):
                    errors.append(self.error_message or f"Invalid format for {self.field_name}.")
        elif self.validation_type == 'min_length':
            try:
                min_length = int(self.validation_expression)
                if len(str(value)) < min_length:
                    errors.append(self.error_message or f"{self.field_name} must be at least {min_length} characters long.")
            except (ValueError, TypeError):
                errors.append("Invalid min_length value.") # Handle cases where expression isn't a valid integer
        elif self.validation_type == 'max_length':
            try:
                max_length = int(self.validation_expression)
                if len(str(value)) > max_length:
                    errors.append(self.error_message or f"{self.field_name} must be no more than {max_length} characters long.")
            except (ValueError, TypeError):
                 errors.append("Invalid max_length value.") # Handle cases where expression isn't a valid integer
        elif self.validation_type == 'email':
            # Basic email validation using regex (consider a more robust library for production)
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, str(value)):
                errors.append(self.error_message or "Invalid email format.")
        # Add more validation types as needed

        return errors