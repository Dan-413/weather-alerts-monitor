import requests
from alerts.base import Alert, AlertProvider

HEADERS = {
    "User-Agent": "weather-alerts-monitor (your-email@example.com)"
}

class NWSProvider(AlertProvider):
    """
    Pulls all active NWS alerts across the U.S. and filters them based on
    provided severities and areas.
    """

    def __init__(self, severities=None, areas=None):
        self.severities = severities or []  # List of selected severities
        self.areas = areas or []            # List of selected area names or states

    def get_alerts(self):
        alert_results = []

        try:
            # Pull all active alerts from the National Weather Service
            url = "https://api.weather.gov/alerts/active"
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()

            for alert in data.get("features", []):
                props = alert["properties"]
                area_desc = props.get("areaDesc", "")  # e.g., "Travis, Williamson, Hays"
                severity = props.get("severity", "Unknown")

                # ✅ AREA FILTER: skip if none of the selected areas match
                if self.areas:
                    if not any(area.lower() in area_desc.lower() for area in self.areas):
                        continue

                # ✅ SEVERITY FILTER: skip if severity not in selected list
                if self.severities:
                    if severity not in self.severities:
                        continue

                alert_results.append(Alert(
                    location=area_desc,
                    event=props.get("event", "Alert"),
                    headline=props.get("headline", "No headline provided"),
                    effective=props.get("effective", ""),
                    expires=props.get("expires", ""),
                    description=props.get("description", "")
                ))

        except Exception as e:
            # Add an alert describing the error
            alert_results.append(Alert(
                location="Nationwide",
                event="NWS Error",
                headline=str(e),
                effective="",
                expires="",
                description=""
            ))

        return alert_results


