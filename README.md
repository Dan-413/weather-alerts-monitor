# Weather Alerts Monitor (Scalable Version)

A modular Flask application that monitors National Weather Service alerts and notifies users via a web interface and email.

## Features
- Modular and scalable architecture
- Periodic background weather alert checks
- Flask web app interface
- Email notifications for active alerts
- Easily configurable for more locations or email options

## Setup

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Edit `mailer.py` with your SMTP credentials.
5. Run the app:
   ```bash
   python app.py
   ```

## Future Enhancements
- Add filters for alert types (e.g., Tornado, Flood)
- Web UI for adding/removing locations
- Export to CSV/JSON or integration with external dashboards
