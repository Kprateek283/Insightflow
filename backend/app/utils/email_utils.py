# app/utils/email_utils.py
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Load from .env

def send_upload_email(to_email: str, alias: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    subject = "📄 Upload Successful – InsightFlow"
    body = f"Hi there!\n\nYour document '{alias}' was uploaded and processed successfully.\n\n– InsightFlow Team"

    message = MIMEText(body)
    message["From"] = smtp_user
    message["To"] = to_email
    message["Subject"] = subject

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
