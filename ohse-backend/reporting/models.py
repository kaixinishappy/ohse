import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
import os

# Create your models here.

class ReportingForm(models.Model):
    INCIDENT_STATUS_CHOICES = [
        ('report_pending_approval', 'Report Pending Approval'),
        ('capa_in_action', 'CAPA In Action'),
        ('investigation_from_gohse', 'Investigation From GOHSE'),
        ('closed', 'Closed'),
        ('rejected_investigation_report', 'Rejected Investigation Report'),
    ]
    APPROVER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    incident_id = models.PositiveIntegerField(primary_key=True)
    reporting_forms = models.JSONField()  # Stores entire JSON blob
    incident_status = models.CharField(max_length=50, default="Pending")
    approver_status = models.CharField(max_length=50, default="Pending")
    is_active = models.BooleanField(default=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)



class ReportingAttachment(models.Model):
    ## can add some logic to set the file type based on the file extension
    FILE_TYPES = [
        ('image', 'Image'),
        ('attachment', 'Attachment'),
    ]

    attachment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident_id = models.ForeignKey('ReportingForm', on_delete=models.CASCADE, related_name='attachments')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

  