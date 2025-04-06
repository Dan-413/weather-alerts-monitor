import smtplib
from email.mime.text import MIMEText

SMTP_SETTINGS = {
    "server": "smtp.gmail.com",
    "port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password",
    "to_email": "destination@example.com"
}

def send_email(subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_SETTINGS["username"]
    msg["To"] = SMTP_SETTINGS["to_email"]

    with smtplib.SMTP(SMTP_SETTINGS["server"], SMTP_SETTINGS["port"]) as server:
        server.starttls()
        server.login(SMTP_SETTINGS["username"], SMTP_SETTINGS["password"])
        server.send_message(msg)
