from pymongo import MongoClient
import pandas as pd

#Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client.project_2

# --------------------------------------------------------------------------------
# query array of all unique stations
stations = db.citibike.distinct("start_station_id")
stations = stations[1:]
# columns we are interested in (dropping mongoDB's _id)
selection = {"start_station_id": 1, "start_station_name": 1, "start_station_latitude": 1, "start_station_longitude": 1, "_id": 0}

# initialize and iterate through unique stations array
unique_stations = []
for station in stations:
    # find station id, and get selected info (lat/lng...ect) and append
    cursor = db.citibike.find_one({"start_station_id": station}, selection)
    unique_stations.append(cursor)

# create stations collection and insert unique_stations
stations_col = db["stations"]
result = stations_col.insert_many(unique_stations)

# --------------------------------------------------------------------------------

# Popular Destinations collection
selection2 = {"end_station_id": 1, "end_station_name": 1, "end_station_latitude": 1, \
                "end_station_longitude": 1, "_id": 0}

popular_destinations = []

for stat in stations: #stations from above
    query = db.citibike.find({"start_station_id": stat}, selection2)
    test = pd.DataFrame(query)
    top_10 = test.groupby(["end_station_id", "end_station_latitude", "end_station_longitude"]\
                        , as_index=False).count().sort_values("end_station_name", ascending=False)[0:10]
    top_10_index = top_10.index.to_list()
    pop_dest = []
    for i in range(len(top_10)):
        dest = {"id": top_10["end_station_id"][top_10_index[i]], \
                "name": test["end_station_name"][top_10_index[i]], \
                "lat": top_10["end_station_latitude"][top_10_index[i]], \
                "lng": top_10["end_station_longitude"][top_10_index[i]], \
                "count": str(top_10["end_station_name"][top_10_index[i]])}
        pop_dest.append(dest)
    record = {"start_station_id": stat, "pop_dest": pop_dest}
    popular_destinations.append(record)

destinations_col = db["popular_destinations"]
result2 = destinations_col.insert_many(popular_destinations)

