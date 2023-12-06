from pydantic import BaseModel
from fastapi import UploadFile

#following are pydantic data model classes used for data validation and basic data structure used for data in transit in user registration APIs

class HealthId(BaseModel):
    healthId : str

class Aadhaar(BaseModel):
    aadhaar : str
    
class Transaction(BaseModel):
    otp : str
    txnId : str

class MobileOTPTransaction(BaseModel):
    txnId : str
    mobile : str

class Details(BaseModel):
    email : str
    firstName : str
    healthId : str
    lastName: str
    middleName : str
    password : str
    profilePhoto : UploadFile
    txnId : str

class RegistrationDetails(BaseModel):
    mobile : str 
    aadhaar : str 

class OneTimePassword(BaseModel):
    otp : str 

class TransactionId(BaseModel):
    txnId : str

class Search(BaseModel):
    mobile: str
    year: str
    name: str
    gender: str