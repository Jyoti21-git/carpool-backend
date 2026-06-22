from pydantic import BaseModel
from pydantic import EmailStr


class SendOtpRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str


class VehicleRequest(BaseModel):
    vehicle_number: str
    vehicle_name: str
    vehicle_type: str
    vehicle_color: str
    max_seats: int


class CompleteProfileRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    department: str
    phone_number: str
    profile_photo: str | None = None

    # vehicles: list[VehicleRequest]
