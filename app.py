from flask import Flask, render_template, request
from alerts.manager import check_alerts
from db.alert_tracker import init_db  # ✅ Import the DB initializer
from scheduler import setup_scheduler

app = Flask(__name__)

# ✅ Initialize DB table at startup
init_db()
setup_scheduler(app)  # Initialize scheduler with your Flask app

@app.route("/")
def index():
    severities = request.args.getlist("severity")
    areas = request.args.getlist("area")

    alerts = check_alerts(severities=severities, areas=areas)
    return render_template(
        "alerts.html",
        alerts=alerts,
        selected_severities=severities,
        selected_areas=areas
    )


if __name__ == "__main__":
    app.run(debug=True)
