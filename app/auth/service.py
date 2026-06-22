import os
import random
import requests

from dotenv import load_dotenv

load_dotenv()


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email: str, otp: str):

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json",
    }

    payload = {
        "sender": {"name": "ST Carpool", "email": "jyoti.pundir2109@gmail.com"},
        "to": [{"email": email}],
        "subject": "ST Carpool - Login Verification Code",
        "htmlContent": f"""
        <h2>ST Carpool</h2>
        <p>Your OTP is:</p>
        <h1>{otp}</h1>
        <p>This OTP is valid for 10 minutes.</p>
        """,
    }

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("BREVO STATUS:", response.status_code)
    print("BREVO RESPONSE:", response.text)
