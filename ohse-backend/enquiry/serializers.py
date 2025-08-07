from rest_framework import serializers
from .validators import EnquirySchemaValidator


class EnquirySerializer(serializers.Serializer):
    data = serializers.JSONField(validators=[EnquirySchemaValidator()])




