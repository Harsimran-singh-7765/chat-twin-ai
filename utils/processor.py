# utils/processor.py

import re
import pandas as pd

def process_chat_file(text):
    lines = text.split("\n")
    pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2})[\u200e]*\s*(AM|PM|am|pm)? - (.*)$')

    messages = []
    current_msg = {"datetime": None, "sender": None, "message": ""}

    for line in lines:
        match = pattern.match(line)
        if match:
            if current_msg["datetime"]:
                messages.append(current_msg)

            date, time, am_pm, body = match.groups()
            dt = f"{date}, {time} {am_pm or ''}".strip()

            if ": " in body:
                sender, msg = body.split(": ", 1)
            else:
                sender, msg = None, body

            current_msg = {"datetime": dt, "sender": sender, "message": msg.strip()}
        else:
            current_msg["message"] += "\n" + line.strip()

    if current_msg["datetime"]:
        messages.append(current_msg)

    df = pd.DataFrame(messages)

    stats = {
        "Total Messages": len(df),
        "Users": df['sender'].nunique(),
        "Top Users": df['sender'].value_counts().head(3).to_dict()
    }

    return stats, df
