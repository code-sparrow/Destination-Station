from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_yelp

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
database = "project_2"
mongo = PyMongo(app, uri=f"mongodb://localhost:27017/{database}")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Return template
    return render_template("index.html")

# Route to render logic.js template using data from Mongo
@app.route("/logic.js")
def logic():

    # Initialize data arrays
    station_data = []
    popular_destination_data = []
    restaurant_data = []

    # query different collections for all records
    for cursor in mongo.db.stations.find({}):
        del cursor["_id"]
        station_data.append(cursor)

    for cursor in mongo.db.popular_destinations.find({}):
        del cursor["_id"]
        popular_destination_data.append(cursor)

    for cursor in mongo.db.restaurants.find({}):
        del cursor["_id"]
        restaurant_data.append(cursor)


    combined_data = [station_data, popular_destination_data, restaurant_data]
    
    # Return template and data
    return render_template("logic.js", combined_data=combined_data)


if __name__ == "__main__":
    app.run(debug=True)