from fastapi import APIRouter, Depends, status, HTTPException, Header
from mongodbconnect.mongodb_connect import car_space_collections
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_user_token, pwd_context
from models.SearchModels import SearchByPostcode, SearchByAddress, SearchBySuburb, AdvancedSearch
import json
from mongodbconnect.mongodb_connect import car_space_collections
from geopy.distance import geodesic 
import pandas as pd
import numpy as np

SearchRouter = APIRouter()

@SearchRouter.post("/search/postcode", tags=["Search Car Spaces"])
async def search_by_postcode(postcode_search: SearchByPostcode):
    filter = {"$or": [{"Postcode": postcode_search.postcode}, {"postcode": postcode_search.postcode}]}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []

    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(postcode_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")

    if limit < len(car_spaces):
        return {"Postcode Search Results": car_spaces[:limit]}

    return {"Postcode Search Results": car_spaces}


@SearchRouter.post("/search/suburb", tags=["Search Car Spaces"])
async def search_by_suburb(suburb_search: SearchBySuburb):
    filter = {"suburb": suburb_search.suburb}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []

    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(suburb_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")

    if limit < len(car_spaces):
        return {"Suburb Search Results": car_spaces[:limit]}\

    return {"Suburb Search Results": car_spaces}


@SearchRouter.post("/search/address", tags=["Search Car Spaces"])
async def search_by_address(address_search: SearchByAddress):
    filter = {"address": address_search.address}
    car_space_cursor = car_space_collections.find(filter)

    car_spaces = []

    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        car_spaces.append(document_dict)

    limit = int(address_search.limit)

    if len(car_spaces) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No car spaces found")

    if limit < len(car_spaces):
        return {"Address Search Results": car_spaces[:limit]}

    return {"Address Search Results": car_spaces}

@SearchRouter.post("/search/advancedsearch", tags=["Search Car Spaces"])
async def advanced_search(advanced_search: AdvancedSearch):
    combined_conditions = []
    advanced_search_dict = advanced_search.dict()

    # Apply basic filtering using "$and" conditions
    for key, value in advanced_search_dict.items():
        if value is None:
            continue
        if key == 'minprice':
            combined_conditions.append({
                "$or": [
                    {"price": {"$gte": int(value)}},
                    {"Price": {"$gte": int(value)}}
            ]})

        elif key == 'maxprice':
            combined_conditions.append({
                "$or": [
                    {"price": {"$lte": int(value)}},
                    {"Price": {"$lte": int(value)}}
            ]})

        elif key == 'spacetype':
            combined_conditions.append({
                "$or": [
                    {"SpaceType": value},
                    {"spacetype": value},
                    {"spaceType": value},
                    {"Spaceype": value},
            ]})

        elif key == 'vehicletype':
            combined_conditions.append({
                "$or": [
                    {"VehicleType": value},
                    {"vehiclesize": value},
                    {"vehicleSize": value},
                    {"Vehiclesize": value}
            ]})
            
    filter = {"$and": combined_conditions} if len(combined_conditions) > 0 else {}
    car_space_cursor = car_space_collections.find(filter)
    filtered_carspaces = []
    for document in car_space_cursor:
        document_str = json.dumps(document, default=str)
        document_dict = json.loads(document_str)
        filtered_carspaces.append(document_dict)

    # Apply Filter on distance From pin based on latitude/longitude, we will use the geodesic function from geopy library
    if advanced_search_dict['latitude'] is not None and advanced_search_dict['longitude'] is not None and advanced_search_dict["distancefrompin"] is not None:
        for car_space in filtered_carspaces:
            latitude = car_space.get('latitude')
            longitude = car_space.get('longitude')
            if latitude is not None and longitude is not None:
                try:
                    geodistance = geodesic(
                        (float(latitude), float(longitude)),
                        (float(advanced_search_dict["latitude"]), float(advanced_search_dict["longitude"]))
                    ).kilometers
                    car_space["geodistance"] = geodistance if geodistance <= float(advanced_search_dict["distancefrompin"]) else None
                except ValueError:
                    car_space["geodistance"] = None
            else:
                car_space["geodistance"] = None

        filtered_carspaces = [obj for obj in filtered_carspaces if obj.get("geodistance") is not None]


    if advanced_search_dict["sortmethod"] is not None and advanced_search_dict["recommendersystem"] is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cannot have a sort method and recommender system in the body")

    sortmethod = advanced_search_dict.get("sortmethod")

    if sortmethod:
        if sortmethod == "price-ascending":
            filtered_carspaces.sort(key=lambda x: x["Price"], reverse=False)

        elif sortmethod == "price-descending":
            filtered_carspaces.sort(key=lambda x: x["Price"], reverse=True)

        elif sortmethod == "distance-from-pin-ascending":
            filtered_carspaces.sort(key=lambda x: x.get("geodistance", float("inf")), reverse=False)

        elif sortmethod == "distance-from-pin-descending":
            filtered_carspaces.sort(key=lambda x: x.get("geodistance", float("inf")), reverse=True)

    # TODO First need to simulate users and spots then we can train a model based on the required metrics
    # THIS IS THE PART where we need to train a model using numpy/pandas
    # recommendermethod = advanced_search_dict.get("recommendersystem")
    # if recommendermethod:
    #     if recommender_method == 'cosine':
    #         pass
    #     elif recommender_method == 'jaccard':
    #         pass
    #     elif recommender_method == 'pearson':
    #         pass    

    # Return results as a limit
    if advanced_search_dict["resultlimit"] is not None:
        filtered_carspaces = filtered_carspaces[:advanced_search_dict["resultlimit"]]

    return {"Message": "Filters successfully applied", "Filtered Car Spaces": filtered_carspaces}
