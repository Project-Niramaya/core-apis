import base64
import requests
from starlette.middleware.cors import CORSMiddleware
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import Form, FastAPI, HTTPException, APIRouter
from .register import sendHTTPRequest


from ..models.loginDataModels import Transaction, OtpVerificationResponse, Login, LoginOtp


txnid_store = {}
token_store = {} # temp storage

router = APIRouter()


def getPublicKey():
    url = "https://healthidsbx.abdm.gov.in/api/v2/auth/cert"
    response = requests.get(url)
    your_public_key_pem = response.content.decode("utf-8")
    recipient_public_key = serialization.load_pem_public_key(your_public_key_pem.encode())
    return recipient_public_key



# Login APIs
@router.post("/loginGenerateOtp")
def loginGenerateOtp(login_otp: LoginOtp):
    url = "https://healthidsbx.abdm.gov.in/api/v2/registration/mobile/login/generateOtp"
    data = {"mobile": login_otp.mobile}
    response = sendHTTPRequest(url, data)
    return response


@router.post("/loginVerifyOtp")
def loginVerifyOtp(transaction: Transaction):
    url = "https://healthidsbx.abdm.gov.in/api/v2/registration/mobile/login/verifyOtp"
    otp_to_encrypt = transaction.otp
    recipient_public_key = getPublicKey()
    encrypted_otp = recipient_public_key.encrypt(
        otp_to_encrypt.encode("utf-8"),
        padding.PKCS1v15()
    )
    enc_otp = base64.b64encode(encrypted_otp).decode("utf-8")
    data = {"otp": enc_otp, "txnId": transaction.txnId}
    response = sendHTTPRequest(url, data)
    token = response['token']
    token_store['token'] = token
    return response


@router.post("/login")
def login(login_info: Login):
    url = "https://healthidsbx.abdm.gov.in/api/v2/registration/mobile/login/userAuthorizedToken"
    data = {"healthId": login_info.healthId, "txnId": login_info.txnId}
    token = token_store.get('token') # token recieved from prev response must be passed in headers below if temp storage not used
    if token is not None:
        headers = {'T-Token': 'Bearer ' + token}
    else:
        raise Exception("Token is missing or invalid")
    response = sendHTTPRequest(url, data, headers)
    return response


# following apis are to hit to log in user through front-end

@router.post("/loginentermobile")
def loginmobile(mobile: str = Form(...)):  # takes the mobile no from the form
    mobileData = {"mobile": mobile}
    m1 = LoginOtp(**mobileData)
    generateOtpResponse = loginGenerateOtp(
        m1)  # bind the data in a pydantic data model object to call generateOtp api to start a new transaction
    txnId = generateOtpResponse["txnId"]
    # txnid_store["txnId"] = txnId # temp storage
    return {"txnId": txnId}


@router.post("/loginenterotp")
def loginotp(txnId: str, otp: str = Form(...)):  # takes the otp from form and take the txnid from previous response and feed here
    # txnId = txnid_store.get("txnId")  # using a temporary storage
    otpVerificationData = {"otp": otp, "txnId": txnId}
    v1 = Transaction(
        **otpVerificationData)  # bind the otp and txnId as pydantic data object to call verifyMobileOtp api
    verifyMobileOtpResponse = loginVerifyOtp(v1)
    # txnid_store["txnId"] = txnId
    return verifyMobileOtpResponse


@router.post("/loginenterhid")
def loginhid(txnId : str, healthId: str = Form(...)):
    # txnId = txnid_store.get("txnId") # temp storage
    logindata = {"healthId": healthId, "txnId": txnId}
    h1 = Login(**logindata)  # bind the hid and txnId as pydantic data object to call login api
    loginresponse = login(h1)
    return loginresponse

# this is the end of login apis
# the token recieved from loginenterhid must be used as X-Token in the user profile apis which will be updated soon or when required
