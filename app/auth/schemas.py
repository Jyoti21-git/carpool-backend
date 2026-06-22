from pydantic import EmailStr
from pydantic import BaseModel


class SendOtpRequest(BaseModel):
    email: EmailStr


class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
