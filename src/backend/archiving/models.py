import uuid
from datetime import datetime
from typing import Optional

from django.db import models

class ArchiveTask(models.Model):
    task_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    data_type = models.CharField(max_length=255, help_text="Type of data being archived (e.g., 'customer_data', 'transaction_logs')")
    s3_bucket = models.CharField(max_length=255, help_text="Name of the S3 bucket")
    s3_key = models.CharField(max_length=1024, help_text="S3 key (path) for the archived data")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('interrupted', 'Interrupted')
    ], default='pending')
    file_size_bytes = models.BigIntegerField(null=True, blank=True, help_text="Size of the archived file in bytes")
    checksum = models.CharField(max_length=255, null=True, blank=True, help_text="Checksum for data integrity verification")
    error_message = models.TextField(blank=True, help_text="Error message if the task failed")
    retries = models.IntegerField(default=0, help_text="Number of retry attempts")
    max_retries = models.IntegerField(default=3, help_text="Maximum number of retry attempts")

    def __str__(self):
        return f"Archive Task ID: {self.task_id}, Status: {self.status}"

    def mark_failed(self, message):
        self.status = 'failed'
        self.error_message = message
        self.end_time = datetime.now()
        self.save()

    def mark_completed(self):
        self.status = 'completed'
        self.end_time = datetime.now()
        self.save()

    def mark_interrupted(self):
        self.status = 'interrupted'
        self.end_time = datetime.now()
        self.save()