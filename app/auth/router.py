from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
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

    await db.execute(delete(OTP).where(OTP.email == request.email))

    db.add(
        OTP(
            email=request.email,
            otp=otp,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )
    )

    await db.commit()

    try:

        send_otp_email(request.email, otp)
        print("EMAIL SENT SUCCESS")
    except Exception as e:
        print("EMAIL ERROR:", str(e))
    return {
        "message": "OTP sent",
    }


@router.post("/verify-otp")
async def verify_otp(
    request: VerifyOtpRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(OTP).where(OTP.email == request.email))

    otp_record = result.scalar_one_or_none()

    if otp_record is None:
        return {
            "success": False,
            "message": "OTP not found",
        }

    if datetime.now(timezone.utc) > otp_record.expires_at:
        await db.delete(otp_record)
        await db.commit()

        return {
            "success": False,
            "message": "OTP expired",
        }

    if otp_record.otp != request.otp:
        return {
            "success": False,
            "message": "Invalid OTP",
        }

    user_result = await db.execute(select(User).where(User.email == request.email))

    user = user_result.scalar_one_or_none()

    if user is None:
        user = User(
            email=request.email,
            is_verified=True,
        )

        db.add(user)

        await db.flush()

    access_token = create_access_token(request.email)

    refresh_token = create_refresh_token(request.email)

    user.refresh_token = refresh_token

    user.refresh_token_expires_at = datetime.now(timezone.utc) + timedelta(days=15)

    await db.delete(otp_record)

    await db.commit()

    return {
        "success": True,
        "message": "OTP verified",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return {
        "email": current_user.email,
        "is_verified": current_user.is_verified,
    }


@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    payload = verify_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    email = payload.get("sub")

    result = await db.execute(select(User).where(User.email == email))

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if (
        user.refresh_token_expires_at
        and datetime.now(timezone.utc) > user.refresh_token_expires_at
    ):
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired",
        )

    if user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token mismatch",
        )

    new_access_token = create_access_token(email)

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.refresh_token = None
    current_user.refresh_token_expires_at = None

    await db.commit()

    return {
        "message": "Logged out",
    }
