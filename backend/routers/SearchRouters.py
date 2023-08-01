from fastapi import APIRouter, Depends, status, HTTPException, Header
from mongodbconnect.mongodb_connect import car_space_collections
from wrappers.wrappers import check_token
from authentication.authentication import generate_token, verify_user_token, pwd_context
from models.SearchModels import SearchByPostcode, SearchByAddress, SearchBySuburb, AdvancedSearch
import json
from mongodbconnect.mongodb_connect import car_space_collections, car_space_review_collections
from geopy.distance import geodesic 
import pandas as pd
import numpy as np
import os 
import random
import re 
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

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
async def advanced_search(advanced_search: AdvancedSearch, 
        token: str = Depends(verify_user_token)):
    if token is None or re.match("^fake_user_[0-9]+$", token) is None:
        userId = random.randint(0, 2000)
    else:
        userId = int(token.split("fake_user_")[1])

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
                    {"SpaceType": value},
            ]})

        elif key == 'vehicletype':
            combined_conditions.append({
                "$or": [
                    {"VehicleType": value},
                    {"vehiclesize": value},
                    {"vehicleSize": value},
                    {"Vehiclesize": value}
            ]})

        elif key == 'suburb':
            combined_conditions.append({"suburb": value})
            
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
            filtered_carspaces.sort(key=lambda x: x.get("price", x.get("Price", float("inf"))), reverse=False)

        elif sortmethod == "price-descending":
            filtered_carspaces.sort(key=lambda x: x.get("price", x.get("Price", float("-inf"))), reverse=True)

        elif sortmethod == "distance-from-pin-ascending":
            filtered_carspaces.sort(key=lambda x: x.get("geodistance", float("inf")), reverse=False)

        elif sortmethod == "distance-from-pin-descending":
            filtered_carspaces.sort(key=lambda x: x.get("geodistance", float("-inf")), reverse=True)

    recommendermethod = advanced_search_dict.get("recommendersystem")

    if recommendermethod:
        carspace_ids = [carspace.get("carspaceid") for carspace in filtered_carspaces]
        query = {"carspaceid": {"$in": carspace_ids}}
        carspace_review_cursor = car_space_review_collections.find(query)

        # Specify the fields you want to include in the DataFrame
        fields_to_include = ["carspaceid", "reviewer_username", "overall"]

        # Create a list of dictionaries containing only the specified fields
        filtered_results = [{field: document[field] for field in fields_to_include if field in document} for document in carspace_review_cursor]

        df = pd.DataFrame(filtered_results)
        df = df[["carspaceid", "overall", "reviewer_username"]].dropna(subset=["reviewer_username"])
        df = df[df["reviewer_username"].str.match("fake_user")]
        df["reviewer_id"] = df["reviewer_username"].str.split("fake_user_").str[1].astype(int)
        df = df[["carspaceid", "overall", "reviewer_id"]]
        df["overall"] = df["overall"].add(1)
        df["overall"] = df["overall"].add(1)

        reader = Reader(rating_scale=(1, 6))
        data = Dataset.load_from_df(df[["reviewer_id", "carspaceid", "overall"]], reader)

        model = SVD()

        trainset = data.build_full_trainset()
        model.fit(trainset)
        carspace_ids = df["carspaceid"].unique()
        predictions = []
        for carspace_id in carspace_ids:
            prediction = model.predict(userId, carspace_id)
            predictions.append((carspace_id, prediction.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        json_dict = {obj['carspaceid']: obj for obj in filtered_carspaces}
        recommender_order_car_spaces = [int(p[0]) for p in predictions]
        filtered_carspaces = [json_dict[id] for id in recommender_order_car_spaces]

    # Return results as a limit
    if advanced_search_dict["resultlimit"] is not None:
        filtered_carspaces = filtered_carspaces[:advanced_search_dict["resultlimit"]] 
    return {"Message": "Filters successfully applied", "Filtered Car Spaces": filtered_carspaces}
