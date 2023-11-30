from fastapi import APIRouter
from ...models.registerDataModels import *
from ..request_utils import sendHTTPRequest

router = APIRouter()    #create instance of APIRouter

#ABHA API endpoints for searching user in ABHA system
#these APIs will be used to check for an existing user in ABHA system

@router.post("/existsByHealthId")                  #api endpoint to check if user exists in ABHA system
def existsByHealthId(healthId : HealthId):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/existsByHealthId"
    data = {"healthId" : healthId.healthId}

    response = sendHTTPRequest(url, data)
    return response