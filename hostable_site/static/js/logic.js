

citibikeData.forEach(d => {
    d.start_station_latitude = +d.start_station_latitude;
    d.start_station_longitude = +d.start_station_longitude;
});
console.log(citibikeData);
console.log(restaurantData);

var layers = {
    SUBWAY_STATIONS: new L.LayerGroup(),
    SUBWAY_LINES: new L.LayerGroup()
};


var stationMarkers = []

citibikeData.forEach(station => {
    // coordinates lat/lng, for circle center
    var coord = [station.start_station_latitude, station.start_station_longitude];
    // push it to the stationMarkers array
    stationMarkers.push(
        L.circle(coord, {
            fillOpacity: 0.7,
            color: "black",
            weight: 0.7,
            fillColor: "black",
            radius: 50,
            className: station.start_station_id 

        }).bindPopup("<h4>" + "Station ID: " + station.start_station_id + "</h4> <hr> <h5>" + station.start_station_name + "</h5>", {'className': 'popupCustom', 'offset': [0, -13]})
    );

});

// markerLayer as feature group for click event listener
var markerLayer = L.featureGroup(stationMarkers);

// set previously clicked layer to null
var prevLayerClicked = null;

// iterate through each station circle and set click event listener
markerLayer.eachLayer(function(layer) {

    layer.on('click', function(){

        // if a circle has been clicked before reset its styles
        if (prevLayerClicked !== null) {

            // Reset style
            prevLayerClicked.setStyle({fillColor: "black", fillOpacity: 0.7});
        }
        // set new style for newly clicked circle
        layer.setStyle({
            fillOpacity: 0.9,
            fillColor: "#239F83",
            radius: 80
        });
        //set pervious layer var to new circle
        prevLayerClicked = layer;
        //get station id of clicked circle from class name
        var selectedStation = layer.options.className;
        console.log(selectedStation);

        // Find clicked station id in restaurant data collection
        function checkID(id) {
            console.log(`hello ${id}`)
            return id.station_id === selectedStation;
        }
        var stationRestaurants = restaurantData.find(checkID);
        console.log(stationRestaurants.restaurants);

        var html = `<h1 style="color: #1B6B73;" id="title">Three Restaurants Nearby: </h1>`;
        stationRestaurants.restaurants.forEach(rest => {

            html +=
                `<div class="row p-4" style="border: 10px solid darkslategrey; border-radius: 7px; margin: 2px;">
                    <div class="col-md-3 img-fluid p-2">
                        <img src="${rest.image_url}" class="picture img-fluid">
                    </div>
                    <div class="col-md-9 p-2">
                        <h3 class="name">${rest.name}</h3>
                        <p>Rating: ${rest.rating}</p>
                        <p>Address: ${rest.display_address}</p>
                        <p>Phone: ${rest.display_phone}</p>
                        <p>Visit Website: <a href="${rest.url}">${rest.name}</a></p>
                    </div>
                </div>`;

        });

        d3.select('#records').html(html);

        
        
    });
});


var streetMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
});


var baseMaps = {
    "Street Map": streetMap
};

// Initialize all of the LayerGroups we'll be using
var overlayMaps = {
    "Bike Stations": markerLayer,
    "Subway Stations": layers.SUBWAY_STATIONS,
    "Subway Lines": layers.SUBWAY_LINES
    //Popular_Destinations: new L.LayerGroup()
};

// Create the map with our layers
var map = L.map("map-id", {
    center: [40.73, -74.0059],
    zoom: 12,
    layers: [streetMap, markerLayer]
});


L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
}).addTo(map);

// Dummy User-Location marker
L.marker([40.73, -74.0059]).addTo(map);


// Subway Lines layer
d3.json("/project-2/hostable_site/static/data/SubwayLines.geojson", function(data) {
        // Creating a geoJSON layer with the retrieved data
        L.geoJson(data, {
        // Style each feature
            style: function(feature) {
                return {
                color: "blue",
                weight: 1.2
                };
        }
        }).addTo(layers.SUBWAY_LINES);
});

// Subway Stations layer
d3.json("/project-2/hostable_site/static/data/SubwayStations.geojson", function(data) {
    // Creating a geoJSON layer with the retrieved data
    L.geoJson(data, {

        pointToLayer: createCustomIcon,

        onEachFeature: function (feature, layer) {
            layer.bindPopup(`${feature.properties.name}<br />
                            Line: ${feature.properties.line}`, {'className' : 'popupCustom'});
        }
    
    }).addTo(layers.SUBWAY_STATIONS);
});

function createCustomIcon (feature, latlng) {
    var smallIcon = new L.Icon({
        iconSize: [36, 36],
        iconAnchor: [18, 36],
        popupAnchor:  [1, -33],
        iconUrl: '/static/images/location.png'
    });

    return L.marker(latlng, { icon: smallIcon })
};
