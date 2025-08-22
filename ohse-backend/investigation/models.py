import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from reporting.models import ReportingForm

# Create your models here.

User = get_user_model()

class Investigation(models.Model):
    investigation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    report = models.ForeignKey(ReportingForm, on_delete=models.CASCADE, related_name='investigations')
    
    investigation_form = models.JSONField()

    # Multiple images
    images = models.ManyToManyField(
        "InvestigationImage",
        blank=True,
        related_name="investigation"
    )

    # Multiple attachments
    attachments = models.ManyToManyField(
        "InvestigationAttachment",
        blank=True,
        related_name="investigation"
    )

    investigator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='investigation'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investigation - {self.investigation_id} - {self.report.incident_status}"

class InvestigationImage(models.Model):
    image = models.ImageField(upload_to="media/investigation/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No Image(s) Uploaded"

class InvestigationAttachment(models.Model):
    file = models.FileField(upload_to="media/investigation/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.file.name) if self.file else "No File(s) Uploaded"

class InvestigationComment(models.Model):
    investigation = models.ForeignKey('Investigation', on_delete=models.CASCADE, related_name='investigation_comments')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)  # Approver who comments

    comment = models.TextField(max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.approver.username} on {self.investigation.investigation_id}"

# class InvestigationsAttachment(models.Model):
#     ## can add some logic to set the file type based on the file extension
#     FILE_TYPES = [
#         ('image', 'Image'),
#         ('attachment', 'Attachment'),
#     ]

#     attachment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     investigation_id = models.ForeignKey('Investigation', on_delete=models.CASCADE, related_name='investigation_attachments')
#     file_type = models.CharField(max_length=20, choices=FILE_TYPES, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

