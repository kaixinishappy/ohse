import uuid
import os
from django.db import models
from django.contrib.auth import get_user_model

from .validators import EnquirySchemaValidator # Custom validator

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

    created_at = models.DateTimeField(auto_now_add=True)

    # 001, 002, ...
    # enquiry_id = models.CharField(
    #     max_length=3,
    #     unique=True,
    #     editable=False
    # )

    # Input based on defined JSON schema
    enquiry_form = models.JSONField(validators=[EnquirySchemaValidator])

    # Multiple images
    images = models.ManyToManyField(
        "EnquiryImage",
        blank=True,
        related_name="enquiries"
    )

    # Multiple attachments
    attachments = models.ManyToManyField(
        "EnquiryAttachment",
        blank=True,
        related_name="enquiries"
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Reporter
    requestor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Approver (assigned later)
    # goshe_manager = models.ForeignKey(
    #     User,
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True,
    #     related_name="approved_enquiries"
    # )

    # goshe_comment = models.TextField(blank=True, null=True)

class EnquiryImage(models.Model):
    image = models.ImageField(upload_to="media/enquiries/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Image {self.id}"
    
    # Display the filename instead of id
    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No Image(s) Uploaded"

class EnquiryAttachment(models.Model):
    file = models.FileField(upload_to="media/enquiries/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Display the filename instead of id
    def __str__(self):
        return os.path.basename(self.file.name) if self.file else "No File(s) Uploaded"

