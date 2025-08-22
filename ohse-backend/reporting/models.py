import uuid
from django.db import models
from django.contrib.auth.models import User
import os

from datetime import datetime

class ReportingForm(models.Model):
    INCIDENT_STATUS_CHOICES = [
        ('pending_investigation_report', 'Pending Investigation Report'), # Investigator hasn't submitted investigation report, only appear when approver has approved the report
        ('under_investigation', 'Under Investigation'), # Investigator has viewed the report
        ('report_pending_approval', 'Report Pending Approval'), # Waiting for GOHSE team to review
        ('capa_in_action', 'CAPA In Action'), # Proceed after investigation form has been approved
        ('closed', 'Closed'), # Case closed/done
        ('rejected_investigation_report', 'Rejected Investigation Report'), # Investigation report is rejected by the GOHSE team, but can edit & resubmit
    ]

    APPROVER_STATUS_CHOICES = [
        ('pending', 'Pending from Approver'), # Waiting for approver to take action
        ('approved', 'Approved'), # Report has been approved by the approver
        ('rejected', 'Rejected'), # Report has been rejected by the approver, but can edit & resubmit
        ('closed', 'Closed'), # Case closed/done
    ]

    # incident_id = models.PositiveIntegerField(
    #     primary_key=True
    # )

    # incident_id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )

    # Custom tracking number in format YY001, YY002, etc.
    tracking_no = models.CharField(max_length=5, unique=True, editable=False, primary_key=True)

    reporting_forms = models.JSONField()

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

    approver_status = models.CharField(
        max_length=50, 
        choices=APPROVER_STATUS_CHOICES,
        default="pending"
    )

    incident_status = models.CharField(
        max_length=50, 
        choices=INCIDENT_STATUS_CHOICES,
        null=True,
        blank=True,
        default=None
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

    def __str__(self):
        return f"Report {self.tracking_no} - Approver: {self.approver_status} - Incident: {self.incident_status}"

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

class ReportingComment(models.Model):
    report = models.ForeignKey('ReportingForm', on_delete=models.CASCADE, related_name='reporting_comments')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)  # Approver who comments

    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.approver.username} on {self.report.tracking_no}"


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
