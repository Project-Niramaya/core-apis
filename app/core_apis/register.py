from fastapi import  Form , UploadFile, APIRouter
from ..models.registerDataModels import *
from .request_utils import sendHTTPRequest
from .ABHA_endpoints.userRegistration import RegistrationService
import logging


router = APIRouter()    #create instance of APIRouter

#logging.basicConfig(level=logging.DEBUG)

reg = RegistrationService()
#following api endpoints are hit to register new user with ABHA from the frontend. All initial data populated from forms. 
   
@router.post("/register")
async def registerNewUser(data : RegistrationDetails): #takes the aadhaar and mobile no from the form
    aadhaarData = {"aadhaar" : data.aadhaar}
    try:
        a1 = Aadhaar(**aadhaarData)
        logging.debug("aadhaar object created")
        generateOtpResponse = reg.generateOtp(a1)   #bind the data in a pydantic data model object to call generateOtp api to start a new transaction
        txnId = generateOtpResponse["txnId"]
        logging.debug("Otp generation successful, txnId returned")
        logging.debug(txnId)
        return {"res" : MobileOTPTransaction(txnId, data.mobile)}
    
    except ValueError as e:
        logging.debug("ValueError occurred in generateOtp") 
    # return MobileOTPTransaction(**txn)    #return the transaction id to the frontend
        

@router.post("/submitOtp")         #obtain otp received as sms from the frontend
def submitOtp(data : OtpSubmission):
    otpData = {"otp" : data.otp, "txnId" : data.txnId}
    try:
        t1 = Transaction(**otpData)         #bind the otp and the transaction id as a pydantic data model object to call verifyOtp
        verifyOtpResponse = reg.verifyOtp(t1)
        txnId = verifyOtpResponse["txnId"]      #transaction id obtained again
        mobileOtpData = {"mobile" : data.mobile, "txnId" : data.txnId}    #bind the txnId and the mobile no as a pydantic data object to call generateMobileOtp
        
        try:
            m1 = MobileOTPTransaction(**mobileOtpData)
            generateMobileOtpResponse = reg.generateMobileOTP(m1)
            txnId = generateMobileOtpResponse["txnId"]
            return {"txnId" : txnId}    #return the txnId obtained to the frontend
        
        except ValueError as e:
            logging.debug("ValueError ocurred in generateMobileOtp")
    
    except ValueError as e:
        logging.debug("ValueError occurred in verifyOtp")              


@router.post("/verifySecondOtp")
def verifySecondOtp(data : Transaction):    #get the second otp received as sms from the frontend form
    otpVerificationData = {"otp" : data.otp, "txnId" : data.txnId}
    try:
        v1 = Transaction(**otpVerificationData)                 #bind the otp and txnId as pydantic data object to call verifyMobileOtp api
        verifyMobileOtpResponse = reg.verifyMobileOTP(v1)
        txnId = verifyMobileOtpResponse["txnId"]
        return {"txnId" : txnId}                                #return the txnId obtained as response to the frontend
    
    except ValueError as e:
        logging.debug("ValueError occurred in verifyMobileOtp")                          


@router.post("/submitRegDetails")                      #obtain all the basic details of the user for registration from the frontend form
def submitRegDetails(data : Details):
    if data.profilePhoto.content_type != "image/jpeg" and data.profilePhoto.content_type != "image/png":
        return {"error": "Only JPEG or PNG images are allowed."}

    if data.profilePhoto.filename.endswith((".jpg", ".jpeg", ".png")):
        return {"error": "File extension not allowed."}

    
    createHealthIdData = {
                            "email" : data.email,              #bind the registration details obtained from the frontend as a pydantic data object
                            "firstname" : data.firstName,
                            "healthId" : data.healthId, 
                            "lastname" : data.lastName, 
                            "middleName" : data.middleName, 
                            "password" : data.password, 
                            "profilePhoto" : data.profilePhoto, 
                            "txnId" : data.txnId                     #txnId returned in the previous api must also be bound in the data object
                        }
    
    try:
        d1 = Details(**createHealthIdData)                              #create pydantic model object
        createHealthIdResponse= reg.createHealthIdWithPreVerified(d1)   #make a call to register the user with ABHA
        return createHealthIdResponse                                   #return the response to the frontend for display
    
    except ValueError as e:
        logging.debug("ValueError occurred in generateHealthIdWithPreverified")
    


    
    
    
     








    


    
    







    





