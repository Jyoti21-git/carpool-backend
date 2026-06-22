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
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:Arial,sans-serif;">

<div style="max-width:600px;margin:0 auto;background:#ffffff;">

    <div style="background:#03234B;padding:30px;text-align:center;color:white;">
        <h1 style="margin:0;font-size:22px;font-weight:bold;">
            ST CARPOOL
        </h1>

        <p style="margin-top:10px;font-size:12px;color:#dbeafe;">
            Secure Employee Commute Platform
        </p>
    </div>

    <div style="padding:50px 35px;text-align:center;">

        <h2 style="margin:0;color:#333333;">
            Verify Your Identity
        </h2>

        <p style="margin-top:18px;color:#666666;font-size:14px;">
            Use the verification code below to securely access your account.
        </p>

        <div style="
            width:190px;
            margin:30px auto;
            padding:18px 0;
            border:1.5px solid #03234B;
            border-radius:12px;
            background:#f8fafc;
            font-size:22px;
            font-weight:bold;
            letter-spacing:6px;
            color:#03234B;
        ">
            {otp}
        </div>

        <p style="color:#666666;font-size:13px;">
            This OTP is valid for 10 minutes.
        </p>

        <p style="margin-top:28px;color:#888888;font-size:13px;">
            If you did not request this verification code, please ignore this email.
        </p>

    </div>

    <div style="
        background:#f5f5f5;
        text-align:center;
        padding:20px;
        color:#666666;
        font-size:12px;
        line-height:1.8;
    ">
        <strong>ST Carpool</strong><br>
        Powered by STMicroelectronics<br>
        © 2026 STMicroelectronics
        <br><br>
        This is an automated system-generated email.
        Please do not reply.
    </div>

</div>

</body>
</html>
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
