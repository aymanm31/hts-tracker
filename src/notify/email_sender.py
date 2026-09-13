import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(subject: str, body: str):
    sender_email = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")
    recipient_email = os.getenv("EMAIL_RECIPIENT")

    if not all([sender_email, app_password, recipient_email]):
        raise RuntimeError("Missing one of SMTP_EMAIL, SMTP_APP_PASSWORD, EMAIL_RECIPIENT")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)