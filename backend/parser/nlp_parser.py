import re
import dateparser
from datetime import datetime, timedelta
import spacy
from .ai_parser import ask_ollama

nlp = spacy.load("en_core_web_sm")

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}

def nth_weekday_after(start_date, target_weekday, n):
    count = 0
    current = start_date
    while True:
        current += timedelta(days=1)
        if current.weekday() == target_weekday:
            count += 1
            if count == n:
                return current

def spacy_parse_deadline(text):
    # Rule: "within X days of [date/event]"
    match = re.search(r"within\s+(\d+)\s+days?\s+of\s+(.+)", text, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        base_text = match.group(2)
        base_date = dateparser.parse(base_text)
        if base_date:
            return {
                "parsed_date": (base_date + timedelta(days=days)).strftime('%Y-%m-%d'),
                "used_ai": False,
                "method": "spacy"
            }

    # Standard NER fallback
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            parsed = dateparser.parse(ent.text)
            if parsed:
                return {
                    "parsed_date": parsed.strftime('%Y-%m-%d'),
                    "used_ai": False,
                    "method": "spacy"
                }
    return None

def parse_deadline(text):
    # 1️⃣ Rule: "X days after Y"
    match = re.search(r"(\d+)\s+days?\s+after\s+(.+)", text, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        base_text = match.group(2)
        base_date = dateparser.parse(base_text)
        if base_date:
            return {
                "parsed_date": (base_date + timedelta(days=days)).strftime('%Y-%m-%d'),
                "used_ai": False,
                "method": "regex"
            }

    # 2️⃣ Rule: "Nth weekday after Y"
    match = re.search(r"(\d+)(st|nd|rd|th)?\s+(\w+day)\s+after\s+(.+)", text, re.IGNORECASE)
    if match:
        nth = int(match.group(1))
        weekday_str = match.group(3).lower()
        base_text = match.group(4)
        base_date = dateparser.parse(base_text)
        weekday = WEEKDAYS.get(weekday_str)
        if base_date and weekday is not None:
            return {
                "parsed_date": nth_weekday_after(base_date, weekday, nth).strftime('%Y-%m-%d'),
                "used_ai": False,
                "method": "regex"
            }

    # 3️⃣ spaCy fallback
    spacy_result = spacy_parse_deadline(text)
    if spacy_result:
        return spacy_result

    # 4️⃣ LLM fallback
    ai_result = ask_ollama(text)
    if ai_result:
        return {
            "parsed_date": ai_result,
            "used_ai": True,
            "method": "ai"
        }

    return None
