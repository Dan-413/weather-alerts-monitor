import requests
from flask import render_template
from mailer import send_email

locations = [
    {"name": "New York, NY", "lat": 40.7128, "lon": -74.0060},
    {"name": "Los Angeles, CA", "lat": 34.0522, "lon": -118.2437},
    {"name": "Chicago, IL", "lat": 41.8781, "lon": -87.6298},
]

HEADERS = {
    "User-Agent": "weather-alerts-script (your-email@example.com)"
}

def get_zone_from_point(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data['properties']['forecastZone']

def get_alerts_for_zone(zone_url):
    url = f"https://api.weather.gov/alerts/active?zone={zone_url.split('/')[-1]}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def check_alerts():
    alert_results = []

    for location in locations:
        try:
            zone_url = get_zone_from_point(location["lat"], location["lon"])
            alerts = get_alerts_for_zone(zone_url)
            if alerts["features"]:
                for alert in alerts["features"]:
                    props = alert["properties"]
                    alert_results.append({
                        "location": location["name"],
                        "event": props["event"],
                        "headline": props["headline"],
                        "effective": props["effective"],
                        "expires": props["expires"],
                        "description": props["description"]
                    })
        except Exception as e:
            alert_results.append({
                "location": location["name"],
                "event": "Error",
                "headline": str(e),
                "effective": "",
                "expires": "",
                "description": ""
            })

    if alert_results:
        email_body = render_template("alerts.html", alerts=alert_results)
        send_email("⚠️ Severe Weather Alerts", email_body)

    return alert_results
