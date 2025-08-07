from jsonschema import validate, ValidationError,FormatChecker
from rest_framework import serializers
import json
import os


class EnquirySchemaValidator:
    def __init__(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'enquiry_schema.json')
        with open(schema_path) as f:
            self.schema = json.load(f)

    def __call__(self, value):
        try:
            validate(instance=value, schema=self.schema, format_checker=FormatChecker())
        except ValidationError as e:
            raise serializers.ValidationError(f"JSON Schema validation error: {e.message}")
        