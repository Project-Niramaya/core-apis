from fastapi import  Form , UploadFile, APIRouter
from ...models.registerDataModels import *
from ..request_utils import sendHTTPRequest

router = APIRouter()


# Following are API endoints for basic apis provided by ABHA sandbox for registration
#these endpoints are used in user registration logic in register.py
@router.post("/generateOtp")
def generateOtp(aadhaar : Aadhaar):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/generateOtp"
    data = {"aadhaar" : aadhaar.aadhaar}

    response = sendHTTPRequest(url, data)
    return response
    

@router.post("/verifyOtp")
def verifyOtp(transaction : Transaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/verifyOTP"
    data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

    response = sendHTTPRequest(url, data)
    return response
    

@router.post("/generateMobileOTP")
def generateMobileOTP(mobileOTPTransaction : MobileOTPTransaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/generateMobileOTP"
    data = {"mobile" : mobileOTPTransaction.mobile, "txnId" : mobileOTPTransaction.txnId}

    response = sendHTTPRequest(url, data)
    return response


@router.post("/verifyMobileOTP")
def verifyMobileOTP(transaction : Transaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/verifyMobileOTP"
    data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

    response = sendHTTPRequest(url, data)
    return response


@router.post("/createHealthIdWithPreVerified")
def createHealthIdWithPreVerified(details : Details):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/createHealthIdWithPreVerified"
    data = {
                details.email, 
                details.firstName, 
                details.healthId, 
                details.lastName, 
                details.middleName, 
                details.password, 
                details.profilePhoto, 
                details.txnId
            }
    
    response = sendHTTPRequest(url, data)
    return response