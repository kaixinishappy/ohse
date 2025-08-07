from django.urls import path
from .views import ReportingFormView

urlpatterns = [
    path("", ReportingFormView.as_view(), name="reporting-form"),
]