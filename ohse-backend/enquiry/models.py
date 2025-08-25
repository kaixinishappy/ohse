import uuid
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Status(models.TextChoices):
    PENDING_SUPPORT = 'pending_support', _('Pending Support From OHSE')
    IN_PROGRESS = 'in_progress', _('Working In Progress')
    CLOSED = 'closed', _('Closed')

class Enquiry(models.Model):
    # STATUS_CHOICES = [
    #     ('pending_support', 'Pending Support From OHSE'), # Status once submitted
    #     ('in_progress', 'Working In Progress'), # Status once GOHSE Team/Manager is viewing
    #     ('closed', 'Closed'), # Status once the enquiry is resolved
    # ]

    # enquiry_id = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )

    enquiry_id = models.CharField(
        max_length=3,
        unique=True,
        editable=False,
        primary_key=True
    )

    # Input based on defined JSON schema
    enquiry_form = models.JSONField()

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING_SUPPORT
    )

    # Reporter
    requestor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enquiries'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.enquiry_id:
            last = Enquiry.objects.order_by('-enquiry_id').first()
            if last and last.enquiry_id.isdigit():
                next_id = int(last.enquiry_id) + 1
            else:
                next_id = 1
            self.enquiry_id = f"{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Enquiry {self.enquiry_id} - {self.status}"



class EnquiryImage(models.Model):
    enquiry = models.ForeignKey("Enquiry", on_delete=models.CASCADE, related_name="enquiry_images")
    image = models.ImageField(upload_to="enquiries/images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.image.name) if self.image else "No Image(s) Uploaded"



class EnquiryAttachment(models.Model):
    enquiry = models.ForeignKey("Enquiry", on_delete=models.CASCADE, related_name="enquiry_attachments")
    file = models.FileField(upload_to="enquiries/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Display the filename instead of id
    def __str__(self):
        return os.path.basename(self.file.name) if self.file else "No File(s) Uploaded"



# Comment section for by GOHSE Team/Manager if they reject the enquiry
class EnquiryComment(models.Model):
    enquiry = models.ForeignKey('Enquiry', on_delete=models.CASCADE, related_name='enquiry_comments')
    approver = models.ForeignKey(User, on_delete=models.CASCADE)  # Approver who comments

    comment = models.TextField(max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.approver.username} on {self.enquiry.enquiry_id}"
    
