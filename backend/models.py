from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    parsed_date = db.Column(db.String(20), nullable=False)
    used_ai = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "parsed_date": self.parsed_date,
            "used_ai": self.used_ai,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
