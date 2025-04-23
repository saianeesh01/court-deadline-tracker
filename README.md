# ⚖️ Court Deadline Tracker

An AI-powered legal productivity tool that helps professionals track and manage court deadlines intelligently.

## ✨ Features

- 🧠 **Natural Language Parsing**  
  Enter phrases like _“Reply due 10 days after April 1”_ and let the system auto-calculate the due date using rule-based NLP and AI fallback.

- 📅 **Google Calendar Integration**  
  Sync deadlines to your personal calendar with email and popup reminders.

- 📨 **2-Week Email Reminders**  
  Get notified automatically via email when a deadline is two weeks away.

- 🛠️ **Edit/Delete with Calendar Sync**  
  Any change to a deadline updates your calendar in real time.

- 🔎 **Filterable & Responsive UI**  
  See AI-generated deadlines, upcoming tasks, and calendar view — all mobile-friendly.

---

## 🧠 Tech Stack

- **Frontend**: React + React-Big-Calendar  
- **Backend**: Flask, Flask-Mail, SQLAlchemy  
- **AI/NLP**: Regex, AI Fallback (Ollama/OpenAI)  
- **Sync**: Google Calendar API + OAuth  
- **Email**: Flask-Mail + APScheduler  
- **Auth**: Firebase (optional) or Flask-Login

---

## 🚀 Setup Instructions

### 🔧 Backend (Flask)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
cp credentials/credentials.json.template credentials/credentials.json  # Add your actual keys
python app.py

```
### Frontend (React)

```bash
cd frontend
npm install
npm start

```

### 🔐 Configuration
Add your Google OAuth credentials to backend/credentials/credentials.json

Create a .env in backend/ for things like:


MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=yourapppassword