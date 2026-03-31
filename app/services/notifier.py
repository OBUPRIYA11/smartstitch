import smtplib
from email.message import EmailMessage

from twilio.rest import Client

from app.config import settings


def notify_order(order_id: int, summary: str) -> dict:
    sms_state = "skipped"
    email_state = "skipped"

    if all(
        [
            settings.twilio_account_sid,
            settings.twilio_auth_token,
            settings.twilio_from_number,
            settings.sms_target_number,
        ]
    ):
        try:
            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            client.messages.create(
                body=f"New SmartStitch order #{order_id}: {summary}",
                from_=settings.twilio_from_number,
                to=settings.sms_target_number,
            )
            sms_state = "sent"
        except Exception:
            sms_state = "failed"

    if all([settings.smtp_username, settings.smtp_password, settings.notification_email_to]):
        try:
            msg = EmailMessage()
            msg["Subject"] = f"SmartStitch order #{order_id}"
            msg["From"] = settings.smtp_username
            msg["To"] = settings.notification_email_to
            msg.set_content(f"Order notification: {summary}")

            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
            email_state = "sent"
        except Exception:
            email_state = "failed"

    return {"sms": sms_state, "email": email_state}
