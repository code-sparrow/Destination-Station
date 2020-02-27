import requests
from pymongo import MongoClient
import pandas as pd

client = MongoClient(port=27017)
db=client.project_2
station = db.stations.find_one({})
print(station)

API_KEY = "Z11wp8COTPXDbWkV9oJi61Rzbb1mED3p-a4MpguUHYDA8KHoJCWk1GrDhqh56_rRbb00O2XHsOejNnjV69gcqNBmiO9dTO2asqvhSR62FPwOPahihGk7u7C7Z5K9XXYx"
ENDPOINT = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": "bearer %s" % API_KEY}

museums = []
for cursor in db.stations.find({}):
    print(cursor)
    PARAMETERS = {"term": "museum",
                    "limit": 5,
                    "radius": 1610,
                    "latitude": cursor['start_station_latitude'],
                    "longitude": cursor["start_station_longitude"]}


    response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

    data = response.json()["businesses"]
    museums.append({"name": data.name, "image_url": data.image_url, "rating": data.rating, "display_address": data.display_address[0], "display_phone": data.display_phone, "url": data.url})


    print(museums)




import requests



API_KEY = ""
ENDPOINT = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": "bearer %s" % API_KEY}

business_type = "museum" # change type here
limit = 3 # how many resaults

PARAMETERS = {"term": business_type,
                "limit": limit,
                "radius": 1610,
                "latitude": cursor['start_station_latitude'],
                "longitude": cursor["start_station_longitude"]} #can use location here, instead of lat/lng


response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)

data = response.json()["businesses"]


print(data)