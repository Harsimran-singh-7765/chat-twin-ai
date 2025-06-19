import os
import time
import shutil
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory

load_dotenv()

# 🧠 Memory for chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_or_create_vectorstore(docs, user):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    index_path = f"vectorstores/{user}"
    chat_path = f"chats/{user}.txt"

    # ✅ If already exists, load from disk
    if os.path.exists(index_path) and os.path.exists(chat_path):
        print("✅ Loading existing vectorstore and chat...")
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    # 🚨 Check if empty docs passed
    if not docs or len(docs) == 0:
        raise ValueError(f"❌ No documents found to create vectorstore for '{user}'")

    print("🧹 Rebuilding vectorstore...")

    # 🔥 Clean old data (if any)
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
    if os.path.exists(chat_path):
        os.remove(chat_path)

    os.makedirs("chats", exist_ok=True)
    os.makedirs("vectorstores", exist_ok=True)

    with open(chat_path, "w", encoding="utf-8") as f:
        for d in docs:
            f.write(d.page_content + "\n")

    # ✅ Now safe to create vectorstore
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(index_path)
    return vectorstore

def ask_persona(query: str, vectorstore, persona_name: str):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

    retriever = vectorstore.as_retriever(
    search_type="mmr",       # more diverse results
    search_kwargs={"k": 20}
    )

    docs = retriever.get_relevant_documents(query)

    # Optional: Add reranking / keyword search later
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are simulating a person named **'{persona_name}'**, based on their WhatsApp messages.

Your job is to **respond like them**, not just copy-paste old messages. You must:
- Speak in their usual tone, mood, slang, or expressions.
- Reference events, jokes, or incidents from their past messages when relevant.
- Maintain consistency in personality (e.g., sarcastic, kind, dry, emotional, etc.).
- Recall things they used to care about, complain about, or mention frequently.
- You are them, because you have their entire chat history as context.

--- PAST CHAT CONTEXT ---
{context}
--------------------------

Now, given this situation or question:
❓ {query}

Respond just like *{persona_name}* would:
"""

    print("🧠 Prompt Preview:\n", prompt[:700])
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)
