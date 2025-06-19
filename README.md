
# 💬 ChatTwin - WhatsApp Style AI Clone using RAG

**ChatTwin** is a fun & emotional AI project that uses your **WhatsApp chat exports** to build an **AI clone** of your friend (or yourself!). It uses **RAG (Retrieval Augmented Generation)** to allow you to *talk to your past* — trained purely on your conversations.

---

## 📌 Features

- 📁 Upload WhatsApp `.txt` chat files
- 📊 Auto-summarize message stats (top users, total messages)
- 🧠 Choose a user from the chat to mimic
- 🧾 Vectorize the chat using FAISS & Google Embeddings
- 🤖 Chat with a Gemini-powered AI clone of your friend
- 💾 Save & reload personas anytime
- 🔐 Password-protected saved persona access

---

## 🧠 Tech Stack

| Tool/Library             | Purpose                         |
|--------------------------|----------------------------------|
| **LangChain**            | RAG pipeline (retriever + LLM)  |
| **Google Gemini**        | Chat model (`gemini-2.0-flash`) |
| **FAISS**                | Local vector database           |
| **Streamlit**            | UI and interface                |
| **GoogleGenerativeAI**   | Embeddings (`embedding-001`)    |
| **Pandas, Regex**        | Parsing WhatsApp chat format    |
| **dotenv**               | Secure API key loading          |

---

## 🚀 How It Works

1. 📤 You upload your exported WhatsApp chat `.txt` file
2. 🧹 The app parses it and separates messages by sender
3. 👤 You select a user to mimic
4. 📚 Their messages are chunked, embedded, and stored in a FAISS vectorstore
5. 🤖 When you ask a question, Gemini uses their context to respond like them!

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/chat-twin-ai.git
cd chat-twin-ai
```
### 2. Create Virtual Environment & Install Requirements
```bash

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```
### 3. Create .env File
```bash 
GEMINI_API_KEY=your_google_gemini_api_key
GOOGLE_API_KEY=your_google_gemini_api_key(same as above)
PERSONA_PANEL_PASS=letmein123
```
### 4. Run the App
```bash
streamlit run main.py
```

## 
📁 File Structure 
chat-twin-ai/                                 
│ 
├── main.py                     # Main Streamlit app                                       
├── .env                        # Your API keys (not pushed to GitHub)                                   
├── requirements.txt            # All dependencies                                   
│                                             
├── utils/                                                            
│   ├── processor.py            # WhatsApp parser & stats                                                       
│   ├── chat_loader.py          # Chunk & prepare documents                                              
│   └── vectorstore.py          # Build/load FAISS vector + Gemini RAG                                                                                                                                                                                         
│                                                                          
├── chats/                      # Stored chat history as text                                                  
└── vectorstores/               # FAISS index folders per user        



## 💡 Limitations
Currently works best with 1-on-1 chats or small groups

May miss messages if WhatsApp format changes (regex based)

The more you chat, the better the personality clone will feel

## 📦 Future Enhancements
🧠 Persona memory + emotion tagging

🗣️ Voice interface (talk to clone)

📱 ChatGPT-like responsive mobile UI

🪄 Multi-user memory mixing (simulate friend groups!)

🧠 Custom fine-tuned LLM on WhatsApp tone


## 🧑‍💻 Author
Made with ❤️ by Harsimran Singh

Just a dev trying to bring AI closer to emotions.

