import uuid
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from django.conf import settings
User = settings.AUTH_USER_MODEL

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.timezone import localtime, timedelta

class IncidentStatus(models.TextChoices):
    PENDING_INVESTIGATION_REPORT = 'pending_investigation_report', _('Pending Investigation Report')
    UNDER_INVESTIGATION = 'under_investigation', _('Under Investigation')
    REPORT_PENDING_APPROVAL = 'report_pending_approval', _('Report Pending Approval')
    CAPA_IN_ACTION = 'capa_in_action', _('CAPA In Action')
    CLOSED = 'closed', _('Closed')
    REJECTED_INVESTIGATION_REPORT = 'rejected_investigation_report', _('Rejected Investigation Report')


class ApproverStatus(models.TextChoices):
    PENDING = 'pending', _('Pending from Approver')
    APPROVED = 'approved', _('Approved')
    REJECTED = 'rejected', _('Rejected')
    CLOSED = 'closed', _('Closed')


RISK_STATUS_MAP = {
    "First aid": "Low Risk",
    "Near Miss": "Low Risk",
    "Lost Time Injury (Other than Bodily Injury – Schedule 1)": "High Risk",
    "Environmental Incident": "High Risk",
    "Occupational Illness": "High Risk",
    "Security Impact": "High Risk",
    "Property Damage": "High Risk",
    "Fatal": "Critical Risk",
    "Lost Time Injury (Bodily Injury – Schedule 1)": "Critical Risk",
    "Dangerous Occurrence": "Critical Risk"
}


class ReportingForm(models.Model):
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

    approver_status = models.CharField(
        max_length=50,
        choices=ApproverStatus.choices,
        default=ApproverStatus.PENDING
    )

    incident_status = models.CharField(
        max_length=50,
        choices=IncidentStatus.choices,
        null=True,
        blank=True,
        default=None
    )

    # Doesn't account for "Other" incident_category
    # Need to set manual risk_status?
    risk_status = models.CharField(max_length=20, editable=False)

    is_active = models.BooleanField(default=True)

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)

    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approvals"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Send email to approver
    def send_approver_email(self):
        victim_name = (
            self.reporting_forms.get("data", {})
            .get("injuredPersons", {})
            .get("name", "Victim")
        )

        tracking_no = self.tracking_no
        approver_link = f"https://yourapp.com/approver/{tracking_no}" # will be defined later
        detail_link = f"https://yourapp.com/report/{tracking_no}" # Will be defined later

        subject = f"[{self.tracking_no} - {self.risk_status}] Incident Report Approval Required"

        context = {
            "victim_name": victim_name,
            "approver_link": approver_link,
            "detail_link": detail_link,
        }

        template_name = None

        if self.risk_status == "Low Risk":
            template_name = "emails/approver/approver_low.txt"

        elif self.risk_status == "High Risk":
            deadline = localtime(self.created_at) + timedelta(days=1)
            context["deadline"] = deadline.strftime("%A, %I:%M %p")
            template_name = "emails/approver/approver_high.txt"

        elif self.risk_status == "Critical Risk":
            deadline = localtime(self.created_at) + timedelta(hours=12)
            context["deadline"] = deadline.strftime("%A, %I:%M %p")
            template_name = "emails/approver/approver_critical.txt"

        if template_name and self.approver and self.approver.email:
            message = render_to_string(template_name, context)
            send_mail(
                subject,
                message,
                "noreply@sunway.com.my",
                [self.approver.email],
                fail_silently=False,
            )


    def save(self, *args, **kwargs):
        if not self.tracking_no:
            year_prefix = str(datetime.now().year)[-2:]
            last = ReportingForm.objects.filter(tracking_no__startswith=year_prefix).order_by('-tracking_no').first()
            next_seq = int(last.tracking_no[-3:]) + 1 if last else 1
            self.tracking_no = f"{year_prefix}{next_seq:03d}"

        # Set risk status based on incident_category
        incidents = self.reporting_forms.get("data", {}).get("incidents", {})
        incident_category = incidents.get("incident_category")

        # print(f"Incident category value: '{incident_category}'")
        self.risk_status = RISK_STATUS_MAP.get(incident_category, "Unknown")

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Report {self.tracking_no} ({self.risk_status}) - Approver: {self.approver_status}"


class ReportingImage(models.Model):
    report = models.ForeignKey('ReportingForm', on_delete=models.CASCADE, related_name='reporting_images')
    image = models.ImageField(upload_to="reporting/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No Image(s) Uploaded"



class ReportingAttachment(models.Model):
    report = models.ForeignKey('ReportingForm', on_delete=models.CASCADE, related_name='reporting_attachments')
    file = models.FileField(upload_to="reporting/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
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
