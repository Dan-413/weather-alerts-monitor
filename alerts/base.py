# alerts/base.py
from typing import List
from dataclasses import dataclass

@dataclass
class Alert:
    location: str
    event: str
    headline: str
    effective: str
    expires: str
    description: str

class AlertProvider:
    def get_alerts(self) -> List[Alert]:
        raise NotImplementedError("Providers must implement get_alerts()")
