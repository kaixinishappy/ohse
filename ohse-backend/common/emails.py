from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

EMAIL_SCENARIOS = {
    "approver_low_risk": {
        "subject": "Incident Case Approval Required - {case_number}",
        "body": "{victim_name} incident case is due for approval."
    },
    "approver_high_risk": {
        "subject": "Incident Case Approval Required (High Risk) - {case_number}",
        "body": "{victim_name} incident case is due for approval by Wednesday, 5.00p.m."
    },
    "approver_critical_risk": {
        "subject": "Incident Case Approval Required (Critical Risk) - {case_number}",
        "body": "{victim_name} incident case is due for approval by Wednesday, 1.00p.m. "
                "Please note that the case must also be notified to DOSH by the quickest means available."
    },
    "approver_reject": {
        "subject": "Incident Case Rejected - {case_number}",
        "body": "{victim_name} incident case is rejected."
    },
    "investigator": {
        "subject": "Incident Case Investigation Required - {case_number}",
        "body": "{victim_name} incident case is due for investigation by Wednesday, 5.00p.m."
    },
    "manager_approve_investigation": {
        "subject": "Investigation Approval Required - {case_number}",
        "body": "{victim_name} incident case is due for approval by Wednesday, 5.00p.m."
    },
    "manager_close": {
        "subject": "Incident Closure Required - {case_number}",
        "body": "{victim_name} incident case is due for closure."
    },
    "gohse_team_update": {
        "subject": "Incident Case Update - {case_number}",
        "body": "{victim_name} incident case is rejected / approved / closed / due for corrective action."
    }
}


def send_incident_email(
    scenario_key,
    case_number,
    victim_name,
    approver_link=None,
    case_link=None,
    edit_link=None,
    to_email=None,
):
    scenario = EMAIL_SCENARIOS[scenario_key]

    subject = scenario["subject"].format(case_number=case_number, victim_name=victim_name)
    body_text = scenario["body"].format(case_number=case_number, victim_name=victim_name)

    context = {
        "SUBJECT": subject,
        "BODY": body_text,
        "CASE_NUMBER": case_number,
        "VICTIM_NAME": victim_name,
        "APPROVER_LINK": approver_link,
        "CASE_LINK": case_link,
        "EDIT_LINK": edit_link,
    }

    message = render_to_string("emails/base_email.txt", context)

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@sunway.com.my"),
        [to_email],
        fail_silently=False,
    )
