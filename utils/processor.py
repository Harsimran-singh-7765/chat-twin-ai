import re
import pandas as pd

def process_chat_file(text):
    lines = text.split("\n")
    # More flexible pattern to support 2-digit year as well
    pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s*(AM|PM|am|pm)?\s*-\s*(.*)$')

    messages = []
    current_msg = {"datetime": None, "sender": None, "message": ""}

    for line in lines:
        match = pattern.match(line)
        if match:
            if current_msg["datetime"]:
                messages.append(current_msg)

            date, time, am_pm, body = match.groups()
            dt = f"{date}, {time} {am_pm or ''}".strip()

            # Try to extract sender
            if ": " in body:
                sender, msg = body.split(": ", 1)
            else:
                sender, msg = None, body  # system messages / media omitted

            current_msg = {"datetime": dt, "sender": sender, "message": msg.strip()}
        else:
            current_msg["message"] += "\n" + line.strip()

    if current_msg["datetime"]:
        messages.append(current_msg)

    df = pd.DataFrame(messages)

    # 👇 Add safety fallback if 'sender' column is missing
    if "sender" not in df.columns or df["sender"].isnull().all():
        return {
            "Total Messages": len(df),
            "Users": 0,
            "Top Users": {}
        }, df

    # ✅ Basic stats
    stats = {
        "Total Messages": len(df),
        "Users": df['sender'].nunique(),
        "Top Users": df['sender'].value_counts().head(3).to_dict()
    }

    return stats, df
