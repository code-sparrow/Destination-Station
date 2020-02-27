import requests
from pymongo import MongoClient
import pandas as pd

client = MongoClient(port=27017)
db=client.project_2
station = db.stations.find_one({})
print(station)

API_KEY = ""
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