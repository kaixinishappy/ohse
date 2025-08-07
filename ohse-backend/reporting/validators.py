from jsonschema import validate, ValidationError, FormatChecker
from rest_framework import serializers
import json
import os
from datetime import date
from dateutil.parser import parse

class ReportingFormSchemaValidator:
    def __init__(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'reporting_form_schema.json')
        with open(schema_path) as f:
            self.schema = json.load(f)

    def __call__(self, value):
        try:
            validate(instance=value, schema=self.schema, format_checker=FormatChecker())
        except ValidationError as e:
            raise serializers.ValidationError(f"JSON Schema validation error: {e.message}")
        # Custom logic can be added here if needed
        today = date.today()

        # Ensure start <= end
        if value["medicalInfo"]['ward_admitted_start_date'] >value["medicalInfo"]['ward_admitted_end_date']:
            raise serializers.ValidationError("Ward admitted start date cannot be after end date.")

        if value["medicalInfo"]['med_cert_start_date'] > value["medicalInfo"]['med_cert_end_date']:
            raise serializers.ValidationError("Medical cert start date cannot be after end date.")
        
        