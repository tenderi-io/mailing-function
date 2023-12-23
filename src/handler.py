import json
import os, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

from src.utils import build_html, build_text, get_email_subject, convert_input


load_dotenv()


def send_verification_email(event, context):
    is_records = event.get("Records")
    records = event['Records'] if is_records else [event]

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    for record in records:
        event = json.loads(record["body"]) if is_records else record
        sender_email = os.getenv("EMAIL_SENDER")
        receiver_email = event["receiver_email"]
        password = os.getenv("EMAIL_PASSWORD")

        inputs = convert_input(event)
        text = build_text(inputs["email_type"])
        html = build_html(
            email_type=inputs["email_type"],
            action_url=inputs["action_url"],
            replacements=inputs["replacements"],
        )

        text_part = MIMEText(text, "plain")
        html_part = MIMEText(html, "html")

        message = MIMEMultipart("alternative")
        message["Subject"] = get_email_subject(inputs["email_type"])
        message["From"] = "Tenderi Cuentas"
        message["To"] = receiver_email
        message.attach(text_part)
        message.attach(html_part)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Login to server and send email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            try:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                raise e

        return f"Email sent to {receiver_email}!"
