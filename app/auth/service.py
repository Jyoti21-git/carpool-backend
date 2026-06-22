import os
import random
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email: str, otp: str):

    msg = EmailMessage()

    msg["Subject"] = "ST Carpool - Login Verification Code"

    msg["From"] = os.getenv("BREVO_SMTP_LOGIN")

    msg["To"] = email

    msg.set_content(f"""
ST Carpool

Your OTP is: {otp}

This OTP is valid for 10 minutes.
""")

    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;padding:20px;">
    <h2>ST Carpool</h2>
    <p>Your OTP is:</p>
    <h1>{otp}</h1>
    <p>This OTP is valid for 10 minutes.</p>
</body>
</html>
""",
        subtype="html",
    )

    with smtplib.SMTP(
        os.getenv("BREVO_SMTP_SERVER"),
        int(os.getenv("BREVO_SMTP_PORT")),
    ) as server:

        server.starttls()

        server.login(
            os.getenv("BREVO_SMTP_LOGIN"),
            os.getenv("BREVO_SMTP_PASSWORD"),
        )

        server.send_message(msg)

    print("BREVO EMAIL SENT")
