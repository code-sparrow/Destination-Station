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

    for cursor in mongo.db.stations.find({}):
        del cursor["_id"]
        station_data.append(cursor)

    for cursor in mongo.db.popular_destinations.find({}):
        del cursor["_id"]
        popular_destination_data.append(cursor)


    combined_data = [station_data, popular_destination_data]
    
    # Return template and data
    return render_template("logic.js", combined_data=combined_data)


# # Route that will trigger the scrape function
# @app.route("/scrape")
# def scrape():

#     # Run the scrape function
#     new_yelp_data = scrape_yelp.scrape()

#     # Update the Mongo database using update and upsert=True
#     # Again: Not sure exactly the MongoDB/Pymongo syntax for referencing a
#     # particular document (in this case yelp) within the collection
#     mongo.db.collection.yelp.update({}, new_yelp_data, upsert=True)

#     # Redirect back to home page
#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)