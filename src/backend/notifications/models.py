import uuid
from datetime import datetime
from typing import Optional
import os
import logging

from django.db import models

logger = logging.getLogger(__name__)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=True, blank=True, help_text="The user this notification is for.  Can be null for system-wide notifications.")
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=[
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ])
    channel = models.CharField(max_length=50, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('system', 'System Log'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Notification: {self.message} - {self.severity} - {self.channel}"

    def mark_sent(self):
        self.sent_at = datetime.now()
        self.save()

    def increment_attempts(self, error_message=None):
        self.attempts += 1
        if error_message:
            self.error_message = error_message
        self.save()

    def should_retry(self):
        return self.attempts < self.max_attempts

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['channel', 'created_at'])
        ]

# Securely store notification credentials (example - replace with a proper secrets management solution)
# This is just a placeholder, do NOT store credentials directly in code!
# Consider using environment variables, a dedicated secrets manager (e.g., HashiCorp Vault),
# or Django's built-in secrets management.

# Example:
# EMAIL_HOST = os.environ.get("EMAIL_HOST")
# SMS_API_KEY = os.environ.get("SMS_API_KEY")