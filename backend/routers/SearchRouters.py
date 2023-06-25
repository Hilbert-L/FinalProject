from fastapi import APIRouter, Depends, status, HTTPException, Header
from mongodbconnect.mongodb_connect import car_space_collections
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_user_token, pwd_context
from models.SearchModels import SearchByPostcode, SearchByAddress, SearchBySuburb
import json

SearchRouter = APIRouter()

@SearchRouter.get("/search/postcode", tags=["Search Car Spaces"])
async def search_by_postcode(postcode_search: SearchByPostcode):
    filter = {"Postcode": postcode_search.postcode}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []
    
    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(postcode_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")
        
    if limit < len(car_spaces):
        return {"Postcode Search Results": car_spaces[:limit]}

    return {"Postcode Search Results": car_spaces}


@SearchRouter.get("/search/suburb", tags=["Search Car Spaces"])
async def search_by_suburb(suburb_search: SearchBySuburb):
    filter = {"Suburb": suburb_search.suburb}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []
    
    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(suburb_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")
        
    if limit < len(car_spaces):
        return {"Suburb Search Results": car_spaces[:limit]}\

    return {"Suburb Search Results": car_spaces}


@SearchRouter.get("/search/address", tags=["Search Car Spaces"])
async def search_by_address(address_search: SearchByAddress):
    filter = {"Address": address_search.address}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []
    
    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(address_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")
        
    if limit < len(car_spaces):
        return {"Address Search Results": car_spaces[:limit]}

    return {"Address Search Results": car_spaces}

    
# TODO General search without recommendor system
# TODO continue with recommendor systems without filtered search
# TODO continue with recommendation systems for filtered search


