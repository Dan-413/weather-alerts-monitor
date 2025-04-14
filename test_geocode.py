from providers.googlemaps import GoogleMapsGeocoder

def main():
    geocoder = GoogleMapsGeocoder()
    location = input("Enter a location (e.g., ZIP, city, or address): ")
    result = geocoder.geocode(location)
    print("Geocoded Location:")
    print(result)

if __name__ == "__main__":
    main()
