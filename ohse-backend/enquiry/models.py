
# Create your models here.
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'Working In Progress'),
        ('pending_support', 'Pending Support From OHSE'),
        ('closed', 'Closed'),
    ]

    enquiry_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    enquiry_form = models.JSONField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    requestor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )
