from rest_framework import serializers
from .validators import EnquirySchemaValidator
from.models import *


class EnquirySerializer(serializers.Serializer):
    data = serializers.JSONField(validators=[EnquirySchemaValidator()])


class EnquiryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryComment
        fields = ['enquiry', 'approver', 'comment', 'created_at']