import os
import requests
from fastapi import FastAPI, HTTPException , APIRouter
from dotenv import load_dotenv


load_dotenv()

router = APIRouter()

clientId = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

@router.post("/getAuthToken")          #API endpoint to get a bearer authorization token to use other apis
def getAuthToken():
    url = "https://dev.abdm.gov.in/gateway/v0.5/sessions"
    data = {"clientId" : clientId, "clientSecret" : clientSecret}

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
        # authToken = getAuthToken()
        
        response =  requests.post(url, headers=headers, json=data)

        if(response.status_code == 200):
            return response.json()
        else:
            return response.json()
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail = str(e))
    