import src.config  # noqa: F401 — loads .env, must be imported first
from src.notify.email_sender import send_email

send_email(
    subject="HTS Tracker — test email",
    body="If you're reading this, the email pipeline works."
)
print("Test email sent.")