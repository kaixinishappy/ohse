from rest_framework import serializers
from .validators import InvestigationSchemaValidator
from datetime import datetime

class InvestigationSerializer(serializers.Serializer):
    data = serializers.JSONField(validators=[InvestigationSchemaValidator()])




