from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReportingForm
from common.emails import send_incident_email

@receiver(post_save, sender=ReportingForm)
def reporting_form_created(sender, instance, created, **kwargs):
    if created:
        victim_name = (
            instance.reporting_forms.get("injuredPersons", [{}])[0].get("name", "Victim")
        )
        case_number = instance.tracking_no
        approver_email = getattr(instance.approver, "email", "approver@example.com")

        send_incident_email(
            scenario_key="approver_low_risk",  # or decide dynamically
            case_number=case_number,
            victim_name=victim_name,
            approver_link=f"https://ohse.sunway.com.my/approve/{case_number}",
            case_link=f"https://ohse.sunway.com.my/report/{case_number}",
            to_email=approver_email,
        )
