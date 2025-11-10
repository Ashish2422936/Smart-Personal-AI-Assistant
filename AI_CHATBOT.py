import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import traceback

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="Jarvis 🤖",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for frontend
st.markdown("""
    <style>
    /* Main chat styling */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Title */
    .title-container {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(90deg, #1f2833, #45a29e);
        color: white;
        margin-bottom: 1rem;
    }

    /* User and model message bubbles */
    .stChatMessage.user {
        background-color: #1f2833 !important;
        color: #66fcf1 !important;
        border-left: 3px solid #45a29e !important;
        border-radius: 10px;
        padding: 0.6rem;
    }

    .stChatMessage.model {
        background-color: #0b0c10 !important;
        color: #c5c6c7 !important;
        border-left: 3px solid #66fcf1 !important;
        border-radius: 10px;
        padding: 0.6rem;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #45a29e !important;
    }

    /* Footer note */
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #777;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
    <div class="title-container">
        <h1>🤖 Jarvis</h1>
        <p>Your personal AI assistant — concise, structured, and smart.</p>
    </div>
""", unsafe_allow_html=True)

# Validate API key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file.")
    st.stop()

# Initialize Gemini Client API
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("🚨 Failed to initialize Gemini Client.")
    st.exception(e)
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# Fine-Tuning
JARVIS_PROMPT = (
    "You are Jarvis — a concise, smart, and polite assistant. "
    "Speak like a helpful professional but stay friendly. "
    "Use short, clear answers (max 3 sentences). "
    "If listing or explaining, format neatly with bullets or numbers."
)

# User Chat input
user_input = st.chat_input("Hi Ashish, How can I assist you today?")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("model"):
        with st.spinner("Jarvis thinking..."):
            try:
                prompt = f"{JARVIS_PROMPT}\n\nUser: {user_input}\nJarvis:"
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                st.markdown(response.text.strip())

            except Exception:
                st.error("An error occurred while getting the response:")
                st.code(traceback.format_exc(), language="python")

# Footer
st.markdown(
    "<div class='footer'>Made using Google Gemini and Streamlit</div>",
    unsafe_allow_html=True
)
