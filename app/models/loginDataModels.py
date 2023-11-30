from pydantic import BaseModel

class Transaction(BaseModel):
    otp: str
    txnId: str


class OtpVerificationResponse(BaseModel):
    success: bool


class Login(BaseModel):
    healthId: str
    txnId: str


class LoginOtp(BaseModel):
    mobile: str