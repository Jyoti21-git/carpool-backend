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
    msg["Subject"] = "Carpool OTP Verification"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = email

    msg.set_content(
        f"Your OTP is: {otp}"
    )

    msg.add_alternative(
        f"""
        <html>
          <body style="font-family:Arial,sans-serif;padding:20px;">
            <h2>Verify your identity</h2>

            <p>Use the OTP below to complete sign in.</p>

            <div style="
              font-size:32px;
              font-weight:bold;
              letter-spacing:10px;
              text-align:center;
              padding:20px;
              border:1px solid #ddd;
              border-radius:8px;
              background:#f8f8f8;
            ">
              {otp}
            </div>

            <p>This OTP is valid for 2 minutes.</p>
          </body>
        </html>
        """,
        subtype="html",
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587,
    ) as server:
        server.starttls()

        server.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD"),
        )

        server.send_message(msg)