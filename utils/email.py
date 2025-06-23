# utils/email_utils.py

import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email: str, subject: str, body: str):
    try:
        email_address = os.getenv("GMAIL_USER")
        email_password = os.getenv("GMAIL_PASSWORD")
        print(f"this is is the email on which trying to send mail{to_email}")

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] = to_email
        
        msg.set_content(body)
        print(f"****************body**********{body}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
