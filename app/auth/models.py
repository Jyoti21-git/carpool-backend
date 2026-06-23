from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship

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

    vehicles = relationship(
        "Vehicle",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    class Vehicle(Base):
        __tablename__ = "vehicles"

        id = Column(
            Integer,
            primary_key=True,
        )

        user_id = Column(
            Integer,
            ForeignKey("users.id"),
            nullable=False,
        )

        vehicle_number = Column(
            String,
            nullable=False,
        )

        vehicle_name = Column(
            String,
            nullable=False,
        )

        vehicle_type = Column(
            String,
            nullable=False,
        )

        vehicle_color = Column(
            String,
            nullable=False,
        )

        max_seats = Column(
            Integer,
            nullable=False,
        )

        user = relationship(
            "User",
            back_populates="vehicles",
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
