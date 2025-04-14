import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GoogleMapsGeocoder:
    """
    Geocodes user-provided location strings using the Google Maps Geocoding API.
    """

    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable.")

    def geocode(self, location_string):
        """
        Converts a location string (ZIP, city, address) into latitude/longitude.
        Returns a dictionary with lat, lon, and formatted address.
        """
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": location_string,
            "key": self.api_key
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            result = data["results"][0]
            lat = result["geometry"]["location"]["lat"]
            lon = result["geometry"]["location"]["lng"]
            formatted = result["formatted_address"]
            return {"lat": lat, "lon": lon, "formatted_address": formatted}
        else:
            raise Exception(f"Geocoding failed: {data['status']}")
