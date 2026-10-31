from django.db import models
import logging

logger = logging.getLogger(__name__)

class EDIDocument(models.Model):
    """
    Represents an EDI document received from a trading partner.
    """
    document_id = models.CharField(max_length=255, unique=True, help_text="Unique identifier for the EDI document.")
    edi_type = models.CharField(max_length=100, help_text="Type of EDI document (e.g., 850, 856).")
    sender_id = models.CharField(max_length=100, help_text="Identifier of the sender.")
    receiver_id = models.CharField(max_length=100, help_text="Identifier of the receiver.")
    file_name = models.CharField(max_length=255, help_text="Original file name of the EDI document.")
    file_content = models.TextField(help_text="Content of the EDI file.")
    processed_datetime = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the document was processed.")
    status = models.CharField(max_length=50, default='RECEIVED', help_text="Status of the EDI document (RECEIVED, PARSED, VALIDATED, PROCESSED, ERROR).")
    error_message = models.TextField(blank=True, null=True, help_text="Error message if any errors occurred during processing.")

    def save(self, *args, **kwargs):
        """
        Override the save method to perform validation and logging.
        """
        if not self.document_id:
            self.document_id = str(hash(self.file_content))  # Generate a hash-based document ID
        
        super().save(*args, **kwargs)
        logger.info(f"EDI Document {self.document_id} saved with status: {self.status}")

    def __str__(self):
        return f"EDI Document ID: {self.document_id}, Type: {self.edi_type}, Status: {self.status}"

class EDISegment(models.Model):
    """
    Represents a segment within an EDI document.
    """
    document = models.ForeignKey(EDIDocument, on_delete=models.CASCADE, related_name='segments', help_text="The EDI document this segment belongs to.")
    segment_id = models.CharField(max_length=10, help_text="Segment identifier (e.g., ISA, GS, ST).")
    segment_data = models.TextField(help_text="Data within the EDI segment.")
    segment_order = models.IntegerField(help_text="The order of the segment within the document.")

    def __str__(self):
        return f"Segment ID: {self.segment_id}, Order: {self.segment_order}, Document: {self.document.document_id}"

class EDIElement(models.Model):
    """
    Represents an element within an EDI segment.
    """
    segment = models.ForeignKey(EDISegment, on_delete=models.CASCADE, related_name='elements', help_text="The EDI segment this element belongs to.")
    element_id = models.CharField(max_length=10, help_text="Element identifier within the segment.")
    element_value = models.CharField(max_length=255, help_text="Value of the EDI element.")

    def __str__(self):
        return f"Element ID: {self.element_id}, Value: {self.element_value}, Segment: {self.segment.segment_id}"