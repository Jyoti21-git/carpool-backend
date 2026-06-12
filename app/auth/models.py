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
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String)
    is_verified = Column(
        Boolean,
        default=False,
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