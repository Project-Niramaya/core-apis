import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from fastapi import Form, FastAPI, HTTPException
from pydantic import BaseModel
import requests
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


txnid_store = {}
token_store = {} # temp storage


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


@app.post("/getAuthToken")  # API endpoint to get a bearer authorization token to use other apis
def getAuthToken():
    url = "https://dev.abdm.gov.in/gateway/v0.5/sessions"
    data = {"clientId": "SBX_004047", "clientSecret": "cbfb6f2a-f0e7-485a-be7b-0de5f5c0b92a"}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["accessToken"]

        else:
            return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


def getPublicKey():
    url = "https://healthidsbx.abdm.gov.in/api/v2/auth/cert"
    response = requests.get(url)
    your_public_key_pem = response.content.decode("utf-8")
    recipient_public_key = serialization.load_pem_public_key(your_public_key_pem.encode())
    return recipient_public_key


def sendHTTPRequest(url: str, data: dict, headers: dict = None):  # common http request method for all apis
    authToken = getAuthToken()
    if headers is None:
        headers = {}
    headers.update({
        'Authorization': 'Bearer ' + authToken,
        'Content-Type': 'application/json'
    })
    try:
        getAuthToken()

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


# Login APIs
@app.post("/loginGenerateOtp")
def loginGenerateOtp(login_otp: LoginOtp):
    url = "https://healthidsbx.abdm.gov.in/api/v2/registration/mobile/login/generateOtp"
    data = {"mobile": login_otp.mobile}
    response = sendHTTPRequest(url, data)
    return response


@app.post("/loginVerifyOtp")
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


@app.post("/login")
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

@app.post("/loginentermobile")
def loginmobile(mobile: str = Form(...)):  # takes the mobile no from the form
    mobileData = {"mobile": mobile}
    m1 = LoginOtp(**mobileData)
    generateOtpResponse = loginGenerateOtp(
        m1)  # bind the data in a pydantic data model object to call generateOtp api to start a new transaction
    txnId = generateOtpResponse["txnId"]
    # txnid_store["txnId"] = txnId # temp storage
    return {"txnId": txnId}


@app.post("/loginenterotp")
def loginotp(txnId: str, otp: str = Form(...)):  # takes the otp from form and take the txnid from previous response and feed here
    # txnId = txnid_store.get("txnId")  # using a temporary storage
    otpVerificationData = {"otp": otp, "txnId": txnId}
    v1 = Transaction(
        **otpVerificationData)  # bind the otp and txnId as pydantic data object to call verifyMobileOtp api
    verifyMobileOtpResponse = loginVerifyOtp(v1)
    # txnid_store["txnId"] = txnId
    return verifyMobileOtpResponse


@app.post("/loginenterhid")
def loginhid(txnId : str, healthId: str = Form(...)):
    # txnId = txnid_store.get("txnId") # temp storage
    logindata = {"healthId": healthId, "txnId": txnId}
    h1 = Login(**logindata)  # bind the hid and txnId as pydantic data object to call login api
    loginresponse = login(h1)
    return loginresponse

# this is the end of login apis
# the token recieved from loginenterhid must be used as X-Token in the user profile apis which will be updated soon or when required
