from ...models.registerDataModels import *
from ..request_utils import sendHTTPRequest
import logging, os
logging.basicConfig(level=logging.DEBUG)

# Following are API endoints for basic apis provided by ABHA sandbox for registration
#these endpoints are used in user registration logic in register.py

class RegistrationService:

    def generateOtp(self, aadhaar : Aadhaar):
        logging.debug("generateOtp called")
        url = os.getenv("GENERATE_OTP")
        data = {"aadhaar" : aadhaar.aadhaar}

        response = sendHTTPRequest(url, data)
        return response
    

    def verifyOtp(self, transaction : Transaction):
        url = os.getenv("VERIFY_OTP")
        data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

        response = sendHTTPRequest(url, data)
        return response
        

    def generateMobileOTP(self, mobileOTPTransaction : MobileOTPTransaction):
        url = os.getenv("GENERATE_MOBILE_OTP")
        data = {"mobile" : mobileOTPTransaction.mobile, "txnId" : mobileOTPTransaction.txnId}

        response = sendHTTPRequest(url, data)
        return response


    def verifyMobileOTP(self, transaction : Transaction):
        url = os.getenv("VERIFY_MOBILE_OTP")
        data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

        response = sendHTTPRequest(url, data)
        return response


    def createHealthIdWithPreVerified(self, details : Details):
        url = os.getenv("CREATE_HEALTH_ID")
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