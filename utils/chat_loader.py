from langchain_core.documents import Document
import re

def load_whatsapp_chat(text):
    # Replace odd unicode space characters
    text = text.replace('\u202f', ' ').replace('\u200e', '')

    lines = text.split('\n')

    pattern = re.compile(
        r'^(?:\[)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2})\s*(AM|PM|am|pm)?(?:\])?\s*[-–]\s*(.*)$'
    )

    docs = []
    current_msg = {"datetime": None, "sender": None, "message": ""}

    for line in lines:
        line = line.strip()
        match = pattern.match(line)
        if match:
            # save the previous one if any
            if current_msg["datetime"] and current_msg["message"]:
                docs.append(Document(
                    page_content=current_msg["message"].strip(),
                    metadata={"sender": current_msg["sender"], "datetime": current_msg["datetime"]}
                ))

            date, time, am_pm, body = match.groups()
            dt = f"{date}, {time} {am_pm or ''}".strip()

            if ": " in body:
                sender, msg = body.split(": ", 1)
            else:
                sender, msg = None, body  # could be system message or media

            current_msg = {
                "datetime": dt,
                "sender": sender,
                "message": msg.strip()
            }
        else:
            # continuation of previous message
            current_msg["message"] += "\n" + line

    # Add last message if it exists
    if current_msg["datetime"] and current_msg["message"]:
        docs.append(Document(
            page_content=current_msg["message"].strip(),
            metadata={"sender": current_msg["sender"], "datetime": current_msg["datetime"]}
        ))

    return docs
