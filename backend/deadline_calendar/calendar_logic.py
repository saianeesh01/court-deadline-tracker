# backend/calendar/calendar_logic.py
from models import Deadline

# In-memory deadline store
deadlines = []

def add_deadline(text, parsed_date, used_ai=False):
    deadline = Deadline(text, parsed_date, used_ai)
    deadlines.append(deadline)
    return deadline.to_dict()


def get_all_deadlines():
    return [d.to_dict() for d in deadlines]
