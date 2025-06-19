import re
import pandas as pd

def process_chat_file(text):
    # Replace weird invisible characters
    text = text.replace('\u202f', ' ').replace('\u200e', '').strip()
    
    lines = text.splitlines()

    # WhatsApp line format (flexible)
    pattern = re.compile(
        r'^(?:\[)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2})\s*(AM|PM|am|pm)?(?:\])?\s*[-–]\s*(.*)$'
    )

    messages = []
    current_msg = {"datetime": None, "sender": None, "message": ""}

    for line in lines:
        line = line.strip()
        match = pattern.match(line)

        if match:
            # Save the previous one before starting a new one
            if current_msg["datetime"]:
                messages.append(current_msg)

            date, time, am_pm, body = match.groups()

            # Normalize date (e.g., 23 => 2023)
            parts = date.split("/")
            if len(parts[2]) == 2:
                parts[2] = "20" + parts[2]
                date = "/".join(parts)

            dt = f"{date}, {time} {am_pm or ''}".strip()

            # Separate sender and message
            if ": " in body:
                sender, msg = body.split(": ", 1)
            else:
                sender, msg = None, body  # System message or media

            current_msg = {
                "datetime": dt,
                "sender": sender,
                "message": msg.strip()
            }

        else:
            # Multi-line message continuation
            if current_msg["message"] != "":
                current_msg["message"] += "\n" + line.strip()

    # Append last message
    if current_msg["datetime"]:
        messages.append(current_msg)

    # Create DataFrame
    df = pd.DataFrame(messages)

    # Clean up DataFrame just in case
    if "sender" not in df.columns or df["sender"].dropna().empty:
        stats = {
            "Total Messages": len(df),
            "Users": 0,
            "Top Users": {}
        }
        return stats, df

    # Calculate stats
    stats = {
        "Total Messages": len(df),
        "Users": df['sender'].nunique(),
        "Top Users": df['sender'].value_counts().head(3).to_dict()
    }

    return stats, df
