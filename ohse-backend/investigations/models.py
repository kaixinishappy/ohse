import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Investigation(models.Model):
    investigation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    investigation_form = models.JSONField()  # stores full JSON structure
    created_at = models.DateTimeField(auto_now_add=True)

    submitter_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='investigations'
    )

class InvestigationsAttachment(models.Model):
    ## can add some logic to set the file type based on the file extension
    FILE_TYPES = [
        ('image', 'Image'),
        ('attachment', 'Attachment'),
    ]

    attachment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investigation_id = models.ForeignKey('Investigation', on_delete=models.CASCADE, related_name='investigation_attachments')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


