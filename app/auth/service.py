import os
import random
import smtplib
import requests
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email: str, otp: str):
    api_key = os.getenv("RESEND_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "from": "onboarding@resend.dev",
        "to": [email],
        "subject": "ST Carpool - Login Verification Code",
        "html": f"""
        <h2>ST Carpool</h2>
        <p>Your OTP is:</p>
        <h1>{otp}</h1>
        <p>This OTP is valid for 10 minutes.</p>
        """,
    }

    response = requests.post(
        "https://api.resend.com/emails",
        headers=headers,
        json=payload,
    )

    print("RESEND STATUS:", response.status_code)
    print("RESEND RESPONSE:", response.text)
