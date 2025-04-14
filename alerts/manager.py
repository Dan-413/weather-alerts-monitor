from alerts.base import Alert
from providers.nws import NWSProvider
from providers.usgs import USGSQuakeProvider
from providers.noaa import NOAAStormProvider

def check_alerts(severities=None, areas=None) -> list[Alert]:
    severities = severities or []
    areas = areas or []

    providers = [
        NWSProvider(severities=severities, areas=areas),
        USGSQuakeProvider(),
        NOAAStormProvider(),
    ]

    all_alerts = []
    for provider in providers:
        alerts = provider.get_alerts()
        all_alerts.extend(alerts)

    return all_alerts
