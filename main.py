import streamlit as st
from dotenv import load_dotenv
import os
from utils.processor import process_chat_file
from utils.chat_loader import load_whatsapp_chat
from utils.vectorstore import get_or_create_vectorstore, ask_persona
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Page config
st.set_page_config(page_title="ChatTwin", page_icon="💬", layout="wide")
st.title("💬 ChatTwin - WhatsApp Style AI")

# Ensure folders exist
os.makedirs("vectorstores", exist_ok=True)
os.makedirs("chats", exist_ok=True)

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "persona" not in st.session_state:
    st.session_state.persona = None

if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False

# -------------------------
# 🔐 Password Protected Panel for Saved Personas
with st.sidebar.expander("🔐 Unlock Saved Personas Panel"):
    password = st.text_input("Enter password to access saved users:", type="password")
    if password == os.getenv("PERSONA_PANEL_PASS", "letmein123"):
        st.success("✅ Access granted")
        st.session_state.auth_ok = True
    elif password != "":
        st.error("❌ Incorrect password")

# -------------------------
# 🧠 Load saved personas (only if access granted)
if st.session_state.auth_ok:
    saved_personas = [f for f in os.listdir("vectorstores") if os.path.isdir(os.path.join("vectorstores", f))]
    if saved_personas:
        st.sidebar.subheader("🧠 Use a Saved Persona")
        selected_saved = st.sidebar.selectbox("Pick from saved users", saved_personas)

        if st.sidebar.button("🪄 Load Persona"):
            st.session_state.vectorstore = FAISS.load_local(
                f"vectorstores/{selected_saved}",
                GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
                allow_dangerous_deserialization=True
            )
            st.session_state.persona = selected_saved
            st.session_state.chat_history = []
            st.success(f"✅ Loaded saved persona: {selected_saved}")

# -------------------------
# 📤 Upload new WhatsApp chat
uploaded_file = st.file_uploader("📁 Upload WhatsApp Chat (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    stats, df = process_chat_file(text)

    st.success("✅ Chat Loaded")
    st.subheader("📊 Summary")
    st.json(stats)

    selected_user = st.selectbox("👤 Select a user to mimic", df['sender'].dropna().unique())

    if selected_user:
        st.markdown(f"💬 Mimicking **{selected_user}**'s style")
        docs = load_whatsapp_chat(text)
        st.session_state.vectorstore = get_or_create_vectorstore(docs, selected_user)
        st.session_state.persona = selected_user
        st.session_state.chat_history = []

# -------------------------------
# 💬 Chat section
if st.session_state.vectorstore:
    st.header(f"🧠 Chat with {st.session_state.persona}'s AI Clone")

    user_query = st.chat_input(f"Ask something to {st.session_state.persona} 👇")

    if user_query:
        st.session_state.chat_history.append(("user", user_query))

        with st.spinner("🤖 Thinking like your friend..."):
            response = ask_persona(user_query, st.session_state.vectorstore, st.session_state.persona)

        st.session_state.chat_history.append(("ai", response))

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)
else:
    st.info("📩 Upload a WhatsApp chat or load a saved user to start chatting.")
