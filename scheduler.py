from apscheduler.schedulers.background import BackgroundScheduler
from alerts import check_alerts

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_alerts, trigger="interval", minutes=60)
    scheduler.start()
