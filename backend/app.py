import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from datetime import datetime

from parser.nlp_parser import parse_deadline
from models import db, Deadline
from flask import redirect, url_for, session
from google_sync.calendar_sync import (
    get_credentials, save_credentials, create_google_event, CREDENTIALS_PATH, SCOPES
)
from google_auth_oauthlib.flow import Flow


# -----------------------------
# Load .env config
# -----------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)

# -----------------------------
# Flask Config (Database + Mail)
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deadlines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True") == "True",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME")),
)

db.init_app(app)
mail = Mail(app)

@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

@app.route("/oauth2callback")
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    flow.fetch_token(authorization_response=request.url)
    save_credentials(flow.credentials)
    return "✅ Google Calendar connected! You can now sync deadlines."

@app.route("/sync_event", methods=["POST"])
def sync_event():
    data = request.get_json()
    text = data.get("text")
    date = data.get("parsed_date")

    try:
        event_link = create_google_event(text, date)
        return jsonify({"message": "Event created", "link": event_link}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Deadline Reminder Logic
# -----------------------------
scheduler = BackgroundScheduler()

def send_deadline_reminders():
    with app.app_context():
        today = datetime.now().date()
        deadlines = Deadline.query.all()

        for d in deadlines:
            due_date = datetime.strptime(d.parsed_date, '%Y-%m-%d').date()
            days_left = (due_date - today).days
            if days_left == 14:
                try:
                    msg = Message(
                        subject="⏰ 2-Week Court Deadline Reminder",
                        recipients=[os.getenv("MAIL_USERNAME")],
                        body=f"""⏳ Reminder: Your deadline is in 2 weeks!

📄 {d.text}
📆 Due on: {d.parsed_date}
"""
                    )
                    mail.send(msg)
                    print(f"🔔 Reminder sent for deadline: {d.text}")
                except Exception as e:
                    print("❌ Reminder email failed:", e)

scheduler.add_job(send_deadline_reminders, 'interval', hours=24)
scheduler.start()

# -----------------------------
# Routes
# -----------------------------
@app.route("/api/parse", methods=["POST"])
def parse():
    data = request.get_json()
    text = data.get("text", "")
    notify = data.get("notify", True)
    result = parse_deadline(text)

    if result and result["parsed_date"]:
        deadline = Deadline(
            text=text,
            parsed_date=result["parsed_date"],
            used_ai=result["used_ai"]
        )
        db.session.add(deadline)
        db.session.commit()

        if notify:
            try:
                msg = Message(
                    subject="📅 New Court Deadline Added",
                    recipients=[os.getenv("MAIL_USERNAME")],
                    body=f"""📄 {text}
📆 Due on: {result['parsed_date']}
🔁 Parsed using: {'AI' if result['used_ai'] else 'Logic'}
"""
                )
                mail.send(msg)
                print("✅ Notification email sent.")
            except Exception as e:
                print("❌ Email failed:", e)

        return jsonify(deadline.to_dict()), 200

    return jsonify({"error": "Could not parse date"}), 400

@app.route("/api/deadlines", methods=["GET"])
def get_deadlines():
    all_deadlines = Deadline.query.order_by(Deadline.parsed_date).all()
    return jsonify([d.to_dict() for d in all_deadlines]), 200

# -----------------------------
# Run the App
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
