from pydantic import BaseModel, EmailStr, Field, validator
from fastapi import UploadFile
import logging


#following are pydantic data model classes used for data validation and basic data structure used for data in transit in user registration APIs
logging.basicConfig(level=logging.DEBUG)

class AadhaarValidator:
    @validator('aadhaar')
    @classmethod
    def validate_aadhaar(cls, aadh):
        if(len(aadh) != 12 or (aadh.isdigit() != True)):
            logging.error("Aadhaar validation error occured in registerDataModels.py")
            raise ValueError("Aadhaar number must contain 12 digits")
        else:
            return aadh
        
class MobileValidator:
    @validator('mobile')
    @classmethod
    def validate_mobile(cls, mobile):
        if(len(mobile) != 10 or (mobile.isdigit() != True)):
            logging.error("Mobile number validation error occured in registerDataModels.py")
            raise ValueError("Mobile number must contain 10 digits")
        else:
            return mobile
        
class OtpValidator:
    @validator('otp')
    @classmethod
    def validate_otp(cls, otp):
        if(len(otp) != 6 or (otp.isdigit() != True)):
            logging.error("OTP validation error occured in OtpValidator class, registerDataModels.py")
            raise ValueError("OTP must contain 6 digits")
        else:
            return otp
        

class HealthId(BaseModel):
    healthId : str

class Aadhaar(BaseModel, AadhaarValidator):
    aadhaar : str

class Transaction(BaseModel, OtpValidator):
    otp : str
    txnId : str

class MobileOTPTransaction(BaseModel, MobileValidator):
    txnId : str
    mobile : str
    
   
        

class Details(BaseModel):
    email : EmailStr
    firstName : str
    healthId : str
    lastName: str
    middleName : str
    password : str = Field(ge=8, le=15)
    profilePhoto : UploadFile
    txnId : str

class RegistrationDetails(BaseModel, MobileValidator, AadhaarValidator):
    mobile : str 
    aadhaar : str 

class OneTimePassword(BaseModel, OtpValidator):
    otp : str 

class TransactionId(BaseModel):
    txnId : str

class Search(BaseModel, MobileValidator):
    mobile: str
    year: str
    name: str
    gender: str

class OtpSubmission(BaseModel, MobileValidator, OtpValidator):
    mobile : str
    txnId : str
    otp : str