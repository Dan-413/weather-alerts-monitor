import requests
from alerts.base import Alert, AlertProvider

class NOAAStormProvider(AlertProvider):
    """
    Pulls active tropical storm data from NOAA's National Hurricane Center JSON feed.
    Parses key details like storm name, advisory headline, and location.
    """

    def get_alerts(self):
        alert_results = []
        url = "https://www.nhc.noaa.gov/CurrentStorms.json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for storm in data.get("storms", []):
                # Basic storm metadata
                name = storm.get("stormName_Nice", "Tropical Storm")
                basin = storm.get("basin", "Unknown Basin")
                storm_type = storm.get("stormType", "Tropical Cyclone")
                advisory = storm.get("publicAdvisory", {}).get("headline", "Public Advisory")
                text = storm.get("publicAdvisory", {}).get("text", "No details available")

                alert_results.append(Alert(
                    location=basin,
                    event=storm_type,
                    headline=f"{name} - {advisory}",
                    effective="",
                    expires="",
                    description=text[:500] + "..."  # Trim to first 500 chars
                ))
        except Exception as e:
            alert_results.append(Alert(
                location="Tropical Regions",
                event="NOAA/NHC Error",
                headline=str(e),
                effective="",
                expires="",
                description=""
            ))

        return alert_results
