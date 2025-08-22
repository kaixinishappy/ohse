from jsonschema import validate, ValidationError, FormatChecker
from rest_framework import serializers
import json
import os
from datetime import datetime

# You'd typically use DRF serializers when:
# You're building a REST API.
# You want to validate incoming JSON requests before processing them.
# You want to transform JSON into Django model instances or vice versa.
# You need custom validation logic (e.g., "end_date must be after start_date").

# Validators can check required field, type, format,minimum length, format constraints enum validation, conditional requirement, custom logic

class InvestigationSchemaValidator:
    def __init__(self, *args, **kwargs):
        schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'investigation_schema.json')
        with open(schema_path) as f:
            self.schema = json.load(f)

    def __call__(self, value):
        try:
            validate(instance=value, schema=self.schema, format_checker=FormatChecker())
        except ValidationError as e:
            raise serializers.ValidationError(f"JSON Schema validation error: {e.message}")
        
    # --- Custom logic below ---
        errors = []

        # Ensure only one team leader
        team_members = value["investigation_team_details"]["team_members"]
        leaders = [m for m in team_members if m.get("is_leader") == True]
        if len(leaders) != 1:
            errors.append("There must be exactly one team leader in 'team_members'.")

        # Ensure unique names across team_members
        names = [m["name"] for m in team_members]
        if len(names) != len(set(names)):
            errors.append("Duplicate team member names found.")

        # Ensure unique names across other_people
        other_names = [p["name"] for p in value["investigation_team_details"]["other_people"]]
        if len(other_names) != len(set(other_names)):
            errors.append("Duplicate 'other_people' names found.")

        # Date comparison: start must be before end
        start = value["investigation_team_details"]["investigation_start_date"]
        end = value["investigation_team_details"]["investigation_end_date"]
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d") # Convert a string into a datetime object
            end_date = datetime.strptime(end, "%Y-%m-%d")
            if start_date > end_date:
                errors.append("investigation_start_date must be before investigation_end_date.")
        except ValueError:
            errors.append("Date format must be YYYY-MM-DD.")

        if errors:
            raise serializers.ValidationError(errors)
        
        # Validate events dates are within investigation period
        for event_type in ["before_incident", "during_incident", "after_incident"]:
            for event in value["events"][event_type]:
                try:
                    event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                    if event_date < start_date or event_date > end_date:
                        errors.append(f"Event date in '{event_type}' must be within investigation period.")
                except ValueError:
                    errors.append(f"Event date format in '{event_type}' must be YYYY-MM-DD.")

        # Validate corrective action dates
        action = value["corrective_preventive_action"]["action"]
        try:
            due_date = datetime.strptime(action["due_date"], "%Y-%m-%d")
            completion_date = datetime.strptime(action["completion_date"], "%Y-%m-%d")
            if completion_date < due_date:
                errors.append("completion_date must not be before due_date in corrective action.")
        except ValueError:
            errors.append("Corrective action dates must be YYYY-MM-DD.")

        # Validate submitter information
        submitter = value["submitter_information"]
        if not submitter["name_of_submitter"].strip():
            errors.append("Submitter name cannot be empty.")
        if not submitter["designation"].strip():
            errors.append("Submitter designation cannot be empty.")
        
        # Validate the date entered is valid or not
        try:
            date = datetime.strptime(submitter["date"], "%Y-%m-%d")
        except ValueError:
            errors.append("Submitter date format must be YYYY-MM-DD.")

