from fastapi import APIRouter
from ...models.registerDataModels import *
from ..request_utils import sendHTTPRequest

router = APIRouter()  # create instance of APIRouter


# ABHA API endpoints for searching user in ABHA system
# these APIs will be used to check for an existing user in ABHA system

@router.post("/existsByHealthId")  # api endpoint to check if user exists in ABHA system
def existsByHealthId(healthId: HealthId):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/existsByHealthId"
    data = {"healthId": healthId.healthId}

    response = sendHTTPRequest(url, data)
    return response


@router.post("/searchByHealthId")  # api endpoint to check if user exists in ABHA system
def searchByHealthId(healthId: HealthId):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/searchByHealthId"
    data = {"healthId": healthId.healthId}

    response = sendHTTPRequest(url, data)
    return response


@router.post("/searchByHealthId")  # api endpoint to check if user exists in ABHA system
def searchByMobile(search: Search):
    url = "https://healthidsbx.abdm.gov.in/api/v1/search/searchByMobile"
    data = {"gender": search.gender, "mobile": search.mobile, "name": search.mobile, "yearOfBirth": search.year}

    response = sendHTTPRequest(url, data)
    return response
