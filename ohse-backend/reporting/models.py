import uuid
from django.db import models
from django.contrib.auth.models import User
import os

from .validators import ReportingFormSchemaValidator # Custom validator
from datetime import datetime

class ReportingForm(models.Model):
    INCIDENT_STATUS_CHOICES = [
        ('report_pending_approval', 'Report Pending Approval'),
        ('capa_in_action', 'CAPA In Action'),
        ('investigation_from_gohse', 'Investigation From GOHSE'),
        ('closed', 'Closed'),
        ('rejected_investigation_report', 'Rejected Investigation Report'),
    ]

    APPROVER_STATUS_CHOICES = [
        ('pending', 'Pending from Approver'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]

    # incident_id = models.PositiveIntegerField(
    #     primary_key=True
    # )

    # incident_id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )

    tracking_no = models.CharField(max_length=5, unique=True, editable=False, primary_key=True)

    reporting_forms = models.JSONField(validators=[ReportingFormSchemaValidator])

    # Multiple images
    images = models.ManyToManyField(
        "ReportingImage",
        blank=True,
        related_name="reporting"
    )

    # Multiple attachments
    attachments = models.ManyToManyField(
        "ReportingAttachment",
        blank=True,
        related_name="reporting"
    )

    incident_status = models.CharField(
        max_length=50, 
        choices=INCIDENT_STATUS_CHOICES,
        default="Pending"
    )

    approver_status = models.CharField(
        max_length=50, 
        choices=APPROVER_STATUS_CHOICES,
        default="Pending"
    )

    # is_active = models.BooleanField(default=True)
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.tracking_no:
            year_prefix = str(datetime.now().year)[-2:]
            last = ReportingForm.objects.filter(tracking_no__startswith=year_prefix).order_by('-tracking_no').first()
            if last:
                last_seq = int(last.tracking_no[-3:])
                next_seq = last_seq + 1
            else:
                next_seq = 1
            self.tracking_no = f"{year_prefix}{next_seq:03d}"
        super().save(*args, **kwargs)

class ReportingImage(models.Model):
    image = models.ImageField(upload_to="media/reporting/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Display the filename instead of id
    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No Image(s) Uploaded"

class ReportingAttachment(models.Model):
    file = models.FileField(upload_to="media/reporting/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Display the filename instead of id
    def __str__(self):
        return os.path.basename(self.file.name) if self.file else "No File(s) Uploaded"


# class ReportingAttachment(models.Model):
#     ## can add some logic to set the file type based on the file extension
#     FILE_TYPES = [
#         ('image', 'Image'),
#         ('attachment', 'Attachment'),
#     ]

#     attachment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     incident_id = models.ForeignKey('ReportingForm', on_delete=models.CASCADE, related_name='attachments')
#     file_type = models.CharField(max_length=20, choices=FILE_TYPES, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
