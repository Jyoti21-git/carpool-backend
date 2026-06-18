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

    msg["From"] = os.getenv("EMAIL_ADDRESS")

    msg["To"] = email

    msg.set_content(f"""
ST Carpool

Your OTP is: {otp}

This OTP is valid for 10 minutes.

If you did not request this OTP,
please ignore this email.
        """)

    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>

<body style="
    margin:0;
    padding:0;
    background:#f5f7fb;
    font-family:Arial,sans-serif;
">

<div style="
    max-width:600px;
    margin:40px auto;
    background:white;
    border-radius:16px;
    overflow:hidden;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
">

    <div style="
        background:#03234B;
        padding:35px;
        text-align:center;
        color:white;
    ">
        <h1 style="
            margin:0;
            font-size:32px;
        ">
            ST CARPOOL
        </h1>

        <p style="
            margin-top:12px;
            opacity:0.95;
            font-size:15px;
        ">
            Drive Together, Save Forever
        </p>
    </div>

    <div style="
        padding:40px;
    ">

        <h2 style="
            text-align:center;
            color:#222;
            margin-top:0;
        ">
            Verify Your Identity
        </h2>

        <p style="
            text-align:center;
            color:#666;
            line-height:1.6;
        ">
            Use the verification code below
            to securely access your account.
        </p>

        <div style="
            margin:35px auto;
            width:240px;
            text-align:center;
            background:#f8f9ff;
            border:2px solid #03234B;
            border-radius:14px;
            padding:22px;
            font-size:36px;
            font-weight:bold;
            letter-spacing:8px;
            color:#03234B;
        ">
            {otp}
        </div>

        <p style="
            text-align:center;
            color:#666;
        ">
            This OTP is valid for
            <strong>10 minutes</strong>.
        </p>

        <p style="
            text-align:center;
            color:#999;
            margin-top:30px;
            font-size:14px;
            line-height:1.6;
        ">
            If you did not request this
            verification code, please
            ignore this email.
        </p>

    </div>

    <div style="
        background:#f8f8f8;
        text-align:center;
        padding:24px;
        color:#777;
        font-size:13px;
        line-height:1.8;
    ">
        <strong>
            ST Carpool
        </strong>

        <br>

        Powered by
        <strong>
            STMicroelectronics
        </strong>

        <br>

        © 2026 STMicroelectronics

        <br><br>

        This is an automated
        system-generated email.
        Please do not reply.
    </div>

</div>

</body>
</html>
        """,
        subtype="html",
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:

        server.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD"),
        )

        server.send_message(msg)
