from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template
from alerts.manager import check_alerts
from mailer import send_email
from db.alert_tracker import init_db, alert_seen, mark_alert_seen
import hashlib

def get_alert_id(alert):
    """
    Generate a unique ID for an alert based on its content.
    We hash the event + headline to track uniqueness.
    """
    unique_str = f"{alert.event}-{alert.headline}"
    return hashlib.sha256(unique_str.encode()).hexdigest()

def scheduled_alert_check(app):
    """
    Main function called by the scheduler.
    - Checks for alerts
    - Filters out duplicates using DB
    - Sends email only if new alerts are found
    """
    with app.app_context():
        alerts = check_alerts()
        new_alerts = []

        for alert in alerts:
            alert_id = get_alert_id(alert)

            if not alert_seen(alert_id):
                new_alerts.append(alert)

                # Mark alert as seen
                mark_alert_seen(
                    alert_id,
                    alert.event,
                    alert.headline,
                    alert.effective or ""
                )

        if new_alerts:
            email_body = render_template("alerts.html", alerts=new_alerts)
            send_email("⚠️ New Weather Alerts", email_body)

def setup_scheduler(app):
    """
    Set up the APScheduler job and start it.
    Also ensures the DB is initialized on startup.
    """
    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: scheduled_alert_check(app),
        trigger="interval",
        minutes=60  # Run every 60 minutes (customize as needed)
    )
    scheduler.start()
