import requests
from alerts.base import Alert, AlertProvider

class USGSQuakeProvider(AlertProvider):
    """
    This provider fetches significant earthquake alerts from the USGS GeoJSON feed.
    It standardizes the earthquake data into the same Alert format used throughout the app.
    """

    def get_alerts(self):
        # USGS feed for significant earthquakes in the last hour
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"
        alert_results = []

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Parse each earthquake as an Alert
            for feature in data.get("features", []):
                props = feature["properties"]
                alert_results.append(Alert(
                    location=props.get("place", "Unknown location"),
                    event="Significant Earthquake",
                    headline=props.get("title", ""),
                    effective=props.get("time", ""),
                    expires="",
                    description=props.get("type", "")
                ))
        except Exception as e:
            # Add a fallback error alert if request fails
            alert_results.append(Alert(
                location="Global",
                event="USGS Error",
                headline=str(e),
                effective="",
                expires="",
                description=""
            ))

        return alert_results
