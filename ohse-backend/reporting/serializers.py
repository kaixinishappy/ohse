from rest_framework import serializers
from .validators import ReportingFormSchemaValidator


class ReportingFormSerializer(serializers.Serializer):
    data = serializers.JSONField(validators=[ReportingFormSchemaValidator()])
