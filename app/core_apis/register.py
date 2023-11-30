from fastapi import  Form , UploadFile, APIRouter

from ..models.registerDataModels import HealthId, Aadhaar, Transaction, TransactionId, OneTimePassword, MobileOTPTransaction, Details, RegistrationDetails
from .request_utils import sendHTTPRequest

router = APIRouter()

#ABHA API endpoints
@router.post("/existsByHealthId")                  #api endpoint to check if user exists in ABHA system
def existsByHealthId(healthId : HealthId):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/existsByHealthId"
    data = {"healthId" : healthId.healthId}

    response = sendHTTPRequest(url, data)
    return response



# Following are API endoints for basic apis provided by ABHA sandbox for registration
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


#following api endpoints are hit to register new user with ABHA from the frontend. All initial data populated from forms. 
   
@router.post("/register")
def registerNewUser(aadhaar : str = Form(...), mobile : str = Form(...)): #takes the aadhaar and mobile no from the form
    aadhaarData = {"aadhaar" : aadhaar}
    a1 = Aadhaar(**aadhaarData)
    generateOtpResponse = generateOtp(a1)   #bind the data in a pydantic data model object to call generateOtp api to start a new transaction
    txnId = generateOtpResponse["txnId"]
    return {"txnId" : txnId, "mobile" : mobile}     #return the transaction id to the frontend

@router.post("/submitOtp")         #obtain otp received as sms from the frontend
def submitOtp(mobile : str, txnId : str, otp : str = Form(...)):
    otpData = {"otp" : otp, "txnId" : txnId}
    t1 = Transaction(**otpData)         #bind the otp and the transaction id as a pydantic data model object to call verifyOtp
    verifyOtpResponse = verifyOtp(t1)
    txnId = verifyOtpResponse["txnId"]      #transaction id obtained again
    mobileOtpData = {"mobile" : mobile, "txnId" : txnId}    #bind the txnId and the mobile no as a pydantic data object to call generateMobileOtp
    m1 = MobileOTPTransaction(**mobileOtpData)
    generateMobileOtpResponse = generateMobileOTP(m1)
    txnId = generateMobileOtpResponse["txnId"]
    return {"txnId" : txnId}                    #return the txnId obtained to the frontend

@router.post("/verifySecondOtp")
def verifySecondOtp(txnId : str, otp : str = Form(...)):    #get the second otp received as sms from the frontend form
    otpVerificationData = {"otp" : otp, "txnId" : txnId}
    v1 = Transaction(**otpVerificationData)                 #bind the otp and txnId as pydantic data object to call verifyMobileOtp api
    verifyMobileOtpResponse = verifyMobileOTP(v1)
    txnId = verifyMobileOtpResponse["txnId"]
    return {"txnId" : txnId}                        #return the txnId obtained as response to the frontend

@router.post("/submitRegDetails")                      #obtain all the basic details of the user for registration from the frontend form
def submitRegDetails(txnId : str,
                    email : str = Form(...), 
                    firstName : str = Form(...),
                    healthId : str = Form(...), 
                    lastName : str = Form(...), 
                    middleName : str = Form(...), 
                    password : str = Form(...), 
                    profilePhoto : UploadFile = Form(...), 
                    ):
    if profilePhoto.content_type != "image/jpeg" and profilePhoto.content_type != "image/png":
        return {"error": "Only JPEG or PNG images are allowed."}

    if profilePhoto.filename.endswith((".jpg", ".jpeg", ".png")):
        return {"error": "File extension not allowed."}

    
    createHealthIdData = {
                            "email" : email,                    #bind the registration details obtained from the frontend as a pydantic data object
                            "firstname" : firstName,
                            "healthId" : healthId, 
                            "lastname" : lastName, 
                            "middleName" : middleName, 
                            "password" : password, 
                            "profilePhoto" : profilePhoto, 
                            "txnId" : txnId                     #txnId returned in the previous api must also be bound in the data object
                        }
    
    d1 = Details(**createHealthIdData)                          #create pydantic model object
    createHealthIdResponse= createHealthIdWithPreVerified(d1)   #make a call to register the user with ABHA
    return createHealthIdResponse                               #return the response to the frontend for display
    


    
    
    
     








    


    
    







    





