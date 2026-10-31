from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ValidationError
import uuid

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if not self.name:
            raise ValidationError("Supplier name cannot be empty.")
        if len(self.name) > 255:
            raise ValidationError("Supplier name is too long.")
        # Input validation to prevent injection attacks.  Sanitize name if needed.
        self.name = self.name.strip() # remove leading/trailing whitespace
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SupplierQuerySet(QuerySet):
    def search(self, query):
        return self.filter(name__icontains=query)

class SupplierManager(models.Manager):
    def get_queryset(self):
        return SupplierQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

class SupplierModel(models.Model):
    objects = SupplierManager()

    class Meta:
        abstract = True
        
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }