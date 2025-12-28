from pathlib import Path
import os

import streamlit as st
from PIL import Image
from dotenv import load_dotenv

from ai_agent import sales_chat
from payments import create_checkout

# =============================
# PAGE CONFIG (MUST BE FIRST)
# =============================
st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="🤖",
    layout="centered"
)

# =============================
# LOAD ENV VARIABLES
# =============================
# Local .env (only for local runs)
load_dotenv()

# Prefer Streamlit Secrets (Cloud), fallback to .env (Local)
PROMPT_PACK_LINK = st.secrets.get("PROMPT_PACK_LINK", os.getenv("PROMPT_PACK_LINK", "")).strip()

# =============================
# SUCCESS / CANCEL HANDLING
# =============================
query = st.query_params

if "success" in query:
    st.success("✅ Payment received! Your download is ready.")
    st.markdown("### 🎁 Download your pack")

    if PROMPT_PACK_LINK:
        st.markdown(f"👉 [Download here]({PROMPT_PACK_LINK})")
    else:
        st.warning("Download link not configured.")

    st.caption("If the link doesn’t open, check your email.")
    st.stop()

if "canceled" in query:
    st.warning("Payment canceled. You can try again anytime.")

# =============================
# STYLING (SAFE CSS)
# =============================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 750px;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    div.stButton > button {
        background: #635BFF !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 700 !important;
        border: none !important;
    }

    div.stButton > button:hover {
        opacity: 0.92;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# LOGO (SAFE LOAD)
# =============================
logo_path = Path(__file__).parent / "logo.png"
if logo_path.exists():
    try:
        st.image(str(logo_path), width=120)
    except Exception:
        st.warning("Logo found but could not be displayed.")

# =============================
# HERO SECTION (STEP 1 – CONVERSION)
# =============================
st.title("🤖 AI Product Sales Assistant")

st.markdown("""
✔ **500+ ready-to-use AI prompts**  
✔ **For beginners (no tech skills)**  
✔ **Works with ChatGPT, Claude, Gemini**  
✔ **Instant download after purchase**
""")

# =============================
# CHAT
# =============================
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask anything about AI products")

if user_input:
    reply = sales_chat(user_input)
    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("AI", reply))

for speaker, msg in st.session_state.chat:
    st.markdown(f"**{speaker}:** {msg}")

# =============================
# BUY SECTION
# =============================
st.subheader("🔥 Buy Now")
st.markdown("### 🔥 Buy once. Use forever.")

if st.button("Buy AI Prompt Mega Pack for Beginners"):
    st.write("✅ Button clicked (debug)")

    try:
        checkout_url = create_checkout("prompt_pack")
        st.write("✅ Checkout URL created:", checkout_url)

        st.success("✅ Redirecting you to secure Stripe checkout...")
        st.link_button("👉 Continue to Stripe Checkout", checkout_url)
        st.stop()

    except Exception as e:
        st.error("❌ Stripe checkout failed. Here is the exact error:")
        st.exception(e)
        st.stop()