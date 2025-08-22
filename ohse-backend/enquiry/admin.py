# from django.contrib import admin
# from django.apps import apps

# # Register your models here.
# # Get all models from the current app
# app_models = apps.get_app_config('enquiry').get_models()

# for model in app_models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass

from django.contrib import admin
from django.apps import apps
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

# Get all models from the current app
app_models = apps.get_app_config('enquiry').get_models()

for model in app_models:
    try:
        class GenericAdmin(admin.ModelAdmin):
            formfield_overrides = {
                models.JSONField: {"widget": JSONEditorWidget},  # JSON editor
            }

        admin.site.register(model, GenericAdmin)
    except admin.sites.AlreadyRegistered:
        pass
