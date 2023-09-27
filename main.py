from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import requests

app = FastAPI()

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
    profilePhoto : str
    txnId : str



@app.post("/getAuthToken")          #API endpoint to get a bearer authorization token to use other apis
def getAuthToken():
    url = "https://dev.abdm.gov.in/gateway/v0.5/sessions"
    data = {"clientId" : "SBX_004047", "clientSecret" : "cbfb6f2a-f0e7-485a-be7b-0de5f5c0b92a"}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["accessToken"]
            
        else:
            return response.json()
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail = str(e))
    


def sendHTTPRequest(url : str, data : dict):        #common http request method for all apis
    authToken = getAuthToken()
    headers = {
                'Authorization': 'Bearer ' + authToken,
                'Content-Type': 'application/json'
            }
    try:
        authToken = getAuthToken()
        
        response =  requests.post(url, headers=headers, json=data)

        if(response.status_code == 200):
            return response.json()
        else:
            return response.json()
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail = str(e))
    


@app.post("/existsByHealthId")                  #api endpoint to check if user exists in ABHA system
def existsByHealthId(healthId : HealthId):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/existsByHealthId"
    data = {"healthId" : healthId.healthId}

    response = sendHTTPRequest(url, data)
    return response



# Following are API enpoints used in registering a new user
@app.post("/generateOtp")
def generateOtp(aadhaar : Aadhaar):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/generateOtp"
    data = {"aadhaar" : aadhaar.aadhaar}

    response = sendHTTPRequest(url, data)
    return response
    

@app.post("/verifyOtp")
def verifyOtp(transaction : Transaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/verifyOTP"
    data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

    response = sendHTTPRequest(url, data)
    return response
    

@app.post("/generateMobileOTP")
def generateMobileOTP(mobileOTPTransaction : MobileOTPTransaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/generateMobileOTP"
    data = {"mobile" : mobileOTPTransaction.mobile, "txnId" : mobileOTPTransaction.txnId}

    response = sendHTTPRequest(url, data)
    return response


@app.post("/verifyMobileOTP")
def verifyMobileOTP(transaction : Transaction):
    url = "https://healthidsbx.abdm.gov.in/api/v1/registration/aadhaar/verifyMobileOTP"
    data = {"otp" : transaction.otp, "txnId" : transaction.txnId}

    response = sendHTTPRequest(url, data)
    return response


@app.post("/createHealthIdWithPreVerified")
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




    





