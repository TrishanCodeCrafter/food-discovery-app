from flask import Blueprint, render_template, request, jsonify
from database import session
from models import Agency
from geopy.geocoders import Nominatim  # Geocoding library to convert addresses to coordinates
from geopy.distance import geodesic
from config import GOOGLE_MAPS_API_KEY # Getting API key from config and passing it to the landing page
import requests

# Create a Flask Blueprint (modular route handling)
api_blueprint = Blueprint("api", __name__)

# Define a route to fetch all agencies
@api_blueprint.route("/agencies", methods=["GET"])
def get_agencies():
    agencies = session.query(Agency).all()
    agency_list = [{"id": agency.id, "name": agency.name} for agency in agencies]
    return jsonify(agency_list)

# Route to fetch a single agency by ID
@api_blueprint.route("/agencies/<string:agency_id>", methods=["GET"])
def get_agency(agency_id):
    agency = session.query(Agency).filter_by(agency_id=agency_id).first()
    if agency:
        return jsonify({"agency id": agency.agency_id, "name": agency.name, "type": agency.type, "Shipping address": agency.address, "phone": agency.phone})
    return jsonify({"error": "Agency not found"}), 404

# Landing Page Route
@api_blueprint.route("/", methods=["GET"])
def landing_page():
    return render_template("index.html", api_key = GOOGLE_MAPS_API_KEY)  # Render landing page with API key for maps

# Search API: Find agencies near a given location
@api_blueprint.route("/search", methods=["GET"])
def search_agencies():
    address = request.args.get("address")  # Get address or ZIP code
    radius = float(request.args.get("radius", 5))  # Default radius = 5 miles
    lat = request.args.get("lat")  # If user selects to filter from their current location
    lng = request.args.get("lng") # If user selects to filter from their current location
    
    
    # if not address:
    #     return jsonify({"error": "Address is required"}), 400


    # geolocator = Nominatim(user_agent="food_assistance_locator")
    # location = geolocator.geocode(address, country_codes="us") # Limit to US locations
    
    if address:
         # Convert address(zipcode to be precise) to lat/lon 
        geolocator = Nominatim(user_agent="food_assistance_locator")
        location = geolocator.geocode(address,  country_codes="us") # Limit to US locations 
        if not location:
            return jsonify({"error": "Location not found"}), 404
        user_coords = (location.latitude, location.longitude)
    elif lat and lng: # If user gave the site their current location
        user_coords = (float(lat), float(lng))    
    else:
        return jsonify({"error": "Address or coordinates are required"}), 400

    # Query agencies from database
    agencies = session.query(Agency).all()
    nearby_agencies = []

    for agency in agencies:
        agency_coords = (agency.latitude, agency.longitude)
        distance = geodesic(user_coords, agency_coords).miles  # Calculate distance

        if distance <= radius:
            nearby_agencies.append({
                "id": agency.id,
                "name": agency.name,
                "latitude": agency.latitude,
                "longitude": agency.longitude,
                "distance": round(distance, 2)
            })

    return jsonify(nearby_agencies)