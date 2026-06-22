from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    password_hash = Column(String)

    is_verified = Column(
        Boolean,
        default=False,
    )

    refresh_token = Column(
        String,
        nullable=True,
    )

    refresh_token_expires_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    first_name = Column(
        String,
        nullable=True,
    )

    last_name = Column(
        String,
        nullable=True,
    )

    department = Column(
        String,
        nullable=True,
    )

    phone_number = Column(
        String,
        nullable=True,
    )

    profile_photo = Column(
        String,
        nullable=True,
    )


class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)

    email = Column(
        String,
        index=True,
        nullable=False,
    )

    otp = Column(
        String,
        nullable=False,
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
