from pydantic import EmailStr
from pydantic import BaseModel


class SendOtpRequest(BaseModel):
    email: EmailStr


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str


class CompleteProfileRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    department: str
    phone_number: str
    profile_photo: str | None = None
