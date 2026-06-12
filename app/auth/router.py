from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token
from app.auth.models import OTP, User
from app.auth.schemas import (
    SendOtpRequest,
    VerifyOtpRequest,
)
from app.auth.service import (
    generate_otp,
    send_otp_email,
)
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/send-otp")
async def send_otp(
    request: SendOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    otp = generate_otp()

    await db.execute(
        delete(OTP).where(
            OTP.email == request.email
        )
    )

    db.add(
        OTP(
            email=request.email,
            otp=otp,
            expires_at=datetime.utcnow()
            + timedelta(minutes=2),
        )
    )

    await db.commit()

    send_otp_email(
        request.email,
        otp,
    )

    return {
        "message": "OTP sent",
    }


@router.post("/verify-otp")
async def verify_otp(
    request: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(OTP).where(
            OTP.email == request.email
        )
    )

    otp_record = result.scalar_one_or_none()

    if otp_record is None:
        return {
            "success": False,
            "message": "OTP not found",
        }

    if otp_record.otp != request.otp:
        return {
            "success": False,
            "message": "Invalid OTP",
        }

    user_result = await db.execute(
        select(User).where(
            User.email == request.email
        )
    )

    user = user_result.scalar_one_or_none()

    if user is None:
        user = User(
            email=request.email,
            is_verified=True,
        )
        db.add(user)

    await db.delete(otp_record)
    await db.commit()

    token = create_access_token(
        request.email
    )

    return {
        "success": True,
        "message": "OTP verified",
        "access_token": token,
        "token_type": "bearer",
    }