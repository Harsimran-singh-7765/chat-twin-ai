# utils/chat_loader.py

from langchain_core.documents import Document
import re

def load_whatsapp_chat(text):
    pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2})[\u200e]*\s*(AM|PM|am|pm)? - (.*)$')

    docs = []
    lines = text.split('\n')

    for line in lines:
        match = pattern.match(line)
        if match:
            date, time, am_pm, body = match.groups()
            dt = f"{date}, {time} {am_pm or ''}".strip()

            if ": " in body:
                sender, msg = body.split(": ", 1)
                metadata = {"sender": sender.strip(), "datetime": dt}
                docs.append(Document(page_content=msg.strip(), metadata=metadata))

    return docs
