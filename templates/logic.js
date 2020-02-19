// Our data from app.py render_template
var citibikeData = {{ combined_data[0] }};
//var yelpData = {{ combined_data[1] }};

citibikeData.forEach(d => {
    d.start_station_latitude = +d.start_station_latitude;
    d.start_station_longitude = +d.start_station_longitude;
});



var stationMarkers = []

citibikeData.forEach(station => {
    // coordinates lat/lng, for circle center
    var coord = [station.start_station_latitude, station.start_station_longitude];
    // push it to the earthquakeMarkers array
    stationMarkers.push(
        L.circle(coord, {
            fillOpacity: 0.7,
            color: "#black",
            weight: 0.7,
            fillColor: "black",
            radius: 70
        })
    );

});
var markerLayer = L.layerGroup(stationMarkers);


// Create the tile layer that will be the background of our map
var lightMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
});

var baseMaps = {
    "Gray Scale": lightMap
};

// Initialize all of the LayerGroups we'll be using
var overlayMaps = {
    Stations: markerLayer
    //Popular_Destinations: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map-id", {
    center: [40.73, -74.0059],
    zoom: 12,
    layers: [lightMap, markerLayer]
});

L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
}).addTo(map);
  