from flask import Flask, render_template
from scheduler import setup_scheduler
from alerts import check_alerts

app = Flask(__name__)

@app.route("/")
def index():
    alerts = check_alerts()
    return render_template("alerts.html", alerts=alerts)

# Initialize the background scheduler
setup_scheduler()

if __name__ == "__main__":
    app.run(debug=True)
