import os
import pickle
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# 📁 OAuth credential paths
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "../credentials/credentials.json")
TOKEN_PATH = "token.pkl"

# 📚 Scopes for calendar event access
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_credentials():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            return pickle.load(token)
    return None

def save_credentials(creds):
    with open(TOKEN_PATH, "wb") as token:
        pickle.dump(creds, token)

def create_google_event(summary, date_str):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "start": {
            "date": date_str,
            "timeZone": "America/New_York",
        },
        "end": {
            "date": date_str,
            "timeZone": "America/New_York",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 60},
            ],
        },
    }

    created = service.events().insert(calendarId="primary", body=event).execute()
    return created.get("htmlLink"), created.get("id")

def update_google_event(event_id, new_summary, new_date_str):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    updated_event = {
        "summary": new_summary,
        "start": {
            "date": new_date_str,
            "timeZone": "America/New_York",
        },
        "end": {
            "date": new_date_str,
            "timeZone": "America/New_York",
        },
    }

    service.events().patch(calendarId="primary", eventId=event_id, body=updated_event).execute()
    print(f"✅ Updated Google Calendar event: {event_id}")

def delete_google_event(event_id):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(calendarId="primary", eventId=event_id).execute()
    print(f"🗑️ Deleted Google Calendar event: {event_id}")
